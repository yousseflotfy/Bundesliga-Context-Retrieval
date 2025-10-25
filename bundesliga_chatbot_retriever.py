import re
import yaml
from qwikidata.sparql import return_sparql_query_results
import wikipediaapi
from langchain.prompts import ChatPromptTemplate

class InvalidInputError(Exception):
    """Custom exception for invalid user input city."""

class WikiAPIError(Exception):
    """Custom exception for invalid user input city."""

def get_bundesliga_clubs():
    """
    Query Wikidata to retrieve all cities in Germany that have clubs
    playing in the Bundesliga (first division).

    Returns:
        dict: A nested dictionary mapping each city to its club information.
            Example:
                {
                    "Munich": {
                        "club_name": "FC Bayern Munich",
                        "club_id": 1234
                    },
                    "Leipzig": {
                        "club_name": "RB Leipzig",
                        "club_id": 5678
                    }
                }

    Raises:
        LookupError: If no clubs are found or if the query fails.
    """


    sparql_query = """
            SELECT DISTINCT ?club ?clubLabel ?city ?cityLabel
            WHERE
            {
            VALUES ?type {wd:Q476028 wd:Q847017 wd:Q103229495 }
            ?club wdt:P31 ?type;
                    wdt:P118 wd:Q82595.
            ?club wdt:P159 ?city
            SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            }
    """
    results = return_sparql_query_results(sparql_query)["results"]["bindings"]
    cities_clubs_dict = {}
    for res in results:
        match = re.search(r'entity/(.*)', res["club"]["value"])
        if not match:
            raise LookupError("Club Not Found")
        club_dict = {"club_name":res["clubLabel"]["value"],"club_id": match.group(1)}
        cities_clubs_dict[res["cityLabel"]["value"]] = club_dict
    return cities_clubs_dict

def question_city_extraction(question:str,cities_clubs_dict:dict):
    """
    Extract the city from a user question and return its Bundesliga club info.

    Args:
        question (str): User question containing the city name.
        cities_clubs_dict (dict): Maps city names to club data.

    Returns:
        club_name:str, club_id:str, city_name:str

    Raises:
        InvalidInputError: If no valid Bundesliga city is found in the question.
    """
    for city in cities_clubs_dict.keys():
        pattern = r'\b' + re.escape(city) + r'\b'
        if  re.search(pattern,question,flags=re.IGNORECASE):
            return cities_clubs_dict.get(city)["club_name"],cities_clubs_dict.get(city)["club_id"] ,city
    raise InvalidInputError("Please Enter a valid city with a team playing in Bundesligue 1.")

def get_coach_name(club:str):
    """
    Query Wikidata to retrieve the current coach of a given club.

    Args:
        club_id (str): wikidata club id

    Returns:
        str: Coach's full name.
    """

    sparql_query = """
    SELECT DISTINCT ?coach ?coachLabel
    WHERE
    {{

    wd:{club} wdt:P286 ?coach.

    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],mul,en". }}
    
    }}
    """
    results = return_sparql_query_results(sparql_query.format(club=club))["results"]["bindings"][0]["coachLabel"]["value"]
    return results

def get_coach_info(coach:str):
    """
    Retrieve a short introduction about a coach using the Wikipedia API.

    Args:
        coach (str): Name of the coach.

    Returns:
        str: Introductory text from the coach's Wikipedia page.
    """
    wiki_wiki = wikipediaapi.Wikipedia(user_agent='Bundesliga-Context-Retrieval', language='en')
    page_py = wiki_wiki.page(coach)
    if not page_py.exists():
        raise WikiAPIError("Wikipedia Page Not Found. Please try again!")
    return page_py.summary

def prompt_formating(city_name:str,club_name:str,coach_name:str,coach_info:str):
    """
    Format the system prompt for the chatbot using data about the city, club, and coach.

    Args:
        city_name (str): Name of the city.
        club_name (str): Name of the football club.
        coach_name (str): Name of the club’s coach.
        coach_info (str): Short Wikipedia introduction about the coach.

    Returns:
        str: Formatted system prompt ready for the LLM.
    """
    with open("prompts.yaml","r",encoding="utf-8") as f:
        prompts = yaml.safe_load(f)
    prompt_template = ChatPromptTemplate.from_template(prompts["chatbot_prompt"])
    system_prompt = prompt_template.format_messages(
        city_name=city_name,
        club_name=club_name,
        coach_name=coach_name,
        coach_info=coach_info
    )
    return system_prompt[0].content

if __name__ == "__main__":
    city_club_dict = get_bundesliga_clubs()
    print("Chatbot: Hi! Type 'exit' to quit.")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break
        
        try:
            club_name,club_id,city_name = question_city_extraction(user_input,city_club_dict)
            coach_name = get_coach_name(club_id)
            coach_info = get_coach_info(coach_name)
            print(prompt_formating(city_name,club_name,coach_name,coach_info))

        except InvalidInputError as e:
            print(f"Chatbot: {e}")
