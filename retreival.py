from qwikidata.sparql import return_sparql_query_results
import spacy
import re
import wikipediaapi

def bundesliga_clubs_retreival():
    """
    Function to query wikidata and construct a dict of cities 
    and clubs playing in the bundesliga 1
    returns: dict
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
            raise Exception("club not found")
        cities_clubs_dict[res["cityLabel"]["value"]] = match.group(1)
    return cities_clubs_dict

def question_city_extraction(question:str,cities_clubs_dict:dict):
    for city in cities_clubs_dict.keys():
        pattern = r'\b' + re.escape(city) + r'\b'
        if re.search(pattern,question,flags=re.IGNORECASE):
            return city, cities_clubs_dict.get(city)

def club_coach_retreival(club:str):
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

def coach_info_retreival(coach:str):
    wiki_wiki = wikipediaapi.Wikipedia(user_agent='Bundesliga-Context-Retrieval', language='en')
    page_py = wiki_wiki.page(coach)
    if not page_py.exists():
        raise Exception("Wikipedia Page Not Found")
    # print(page_py.summary)
    return page_py.summary

def wrapper(question:str,city_club_dict):
    city,club = question_city_extraction(question,city_club_dict)
    coach = club_coach_retreival(club)
    return coach_info_retreival(coach)


if __name__ == "__main__":
    city_club_dict = bundesliga_clubs_retreival()
    print("Chatbot: Hi! Type 'exit' to quit.")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break
        
        # simple response logic
        response = wrapper(user_input,city_club_dict)
        print(f"Chatbot: {response}")

# print(club_coach_retreival("wd:Q15789"))
# print(question_city_extraction("Who is coaching Munich?",bundesliga_clubs_retreival().keys()))