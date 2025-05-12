from fastmcp import FastMCP
from dotenv import load_dotenv
import os
import requests
import json
from typing import Annotated
from pydantic import Field
import asyncio
load_dotenv()

# create the FastMCP instance
mcp = FastMCP(
  name = "mcp_tools_server",
  host = "127.0.0.1",
  port = 8050,
)

async def run_mcp_server():
   """
   This function runs the MCP server instance.
   """
   await mcp.run_async(transport="streamable-http")

   

# define the cache file path
CACHE_FILE = "vocabulary_cache.json"

@mcp.tool()
def initialize_and_read_cache() -> dict:
    """
    Ensures the cache file exists. If not, creates an empty cache file. Then, it reads the cache file so the model will have access to the known words vocabulary. Call this every time the user starts a new chat session, sends you a first message etc. Every Chinese word you use in the chat, should always be checked against the vocabulary (cache) so you'll be able to tell wether or not the user knows it already.
    """
    if not os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'w') as file:
            json.dump([], file)  # Initialize with an empty list
        return {}

    else:
        with open(CACHE_FILE, 'r') as file:
            words = json.load(file)
        return words

@mcp.tool()
def write_to_cache(
   words_list: Annotated[list[str], Field(description="a list of Chinese words that you used in the chat. the words inside the list are strings, and should be unique.")]
   ) -> None:
    """
    Adds new words to the cache file if they don't already exist. Call this every time you recognize new Chinese words that the user has just learned and memorized.
    """
    with open(CACHE_FILE, 'r') as file:
        words = json.load(file)
  
    for word in words_list:
      if word not in words:
          words.append(word)
    
    with open(CACHE_FILE, 'w') as file:
        json.dump(words, file)
    
@mcp.tool()
def get_categories() -> list:
    """
    Gets all the possible categories for the news API. Call this when you want to get the categories of the news API. You will use this function when you decide to start a lesson based on the news, probably because the user requested it.
    """
    
    possible_categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
    return possible_categories


def get_headlines_response_by_category(category):
    """
    get the top headlines by specified category
    """
    news_api_key = os.getenv('NEWS_API_KEY')
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": news_api_key,
        "category": category,
        "pageSize": 5
    }
    
    # get the titles 
    response = requests.get(url, params=params)

    return response.json()

def get_titles_and_description_from_response(headlines_json_response):
    """
    construct a dictionary containing for each article its title and description
    """
    # aggregate titles into a list 
    articles_dict = {}
    for article in headlines_json_response['articles']:
        articles_dict[article['title']] = article['description'] if article['description'] else "no_description"

    return articles_dict

@mcp.tool()
def get_articles_with_category(category):
    """
    get the top headlines by specified category
    """

    headlines_json_response = get_headlines_response_by_category(category)
    articles_dict = get_titles_and_description_from_response(headlines_json_response)
    
    return articles_dict

@mcp.tool()
def get_linkedin_profile_data(
    linkedin_url: Annotated[str, Field(description="the url of the Linkedin profile the user will provide you when asking to learn how to introduce himself in Chinese or asking to base the lesson on any Linkedin profile")]
    ) -> dict:
    """
    get the data of a Linkedin profile provided by the user. You should call this function when the user asks to learn how to introduce himself in Chinese, or if he just asks to base the lesson on any Linkedin profile. Be aware that the user is the one who provides the url of the profile.
    """

    rapidapi_key = os.getenv('RAPIDAPI_KEY')
    url = "https://fresh-linkedin-profile-data.p.rapidapi.com/get-linkedin-profile"

    querystring = {"linkedin_url":linkedin_url,
               "include_skills":"false",
               "include_certifications":"false",
               "include_publications":"false",
               "include_honors":"false",
               "include_volunteers":"false",
               "include_projects":"false",
               "include_patents":"false",
               "include_courses":"false",
               "include_organizations":"false",
               "include_profile_status":"false",
               "include_company_public_url":"false"}
    
    headers = {
	"x-rapidapi-key": rapidapi_key,
	"x-rapidapi-host": "fresh-linkedin-profile-data.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)

    return response.json()['data']


# run the mcp server
if __name__ == "__main__":
  asyncio.run(run_mcp_server())