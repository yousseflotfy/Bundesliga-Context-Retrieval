from qwikidata.sparql import return_sparql_query_results

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
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],mul,en". }
            
            }
    """
    results = return_sparql_query_results(sparql_query)["results"]["bindings"]
    cities_clubs_dict = {}

    for res in results:
        cities_clubs_dict[res["cityLabel"]["value"]] = res["clubLabel"]["value"]
    return cities_clubs_dict

def question_city_extraction(question:str,cities_clubs_dict:dict):
    """
    Function that extracts city from the user questuon
    args: question (str)
          cities_clubs_dict (dict)
    returns: tupe(str,str)
    """
    words_list = question.split()
    for word in words_list:
        if cities_clubs_dict.get(word):
            return cities_clubs_dict.get(word)

print(question_city_extraction("coach of München",bundesliga_clubs_retreival()))