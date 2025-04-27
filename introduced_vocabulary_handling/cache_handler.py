import json
from introduced_vocabulary_handling.cache_handler import *
import requests
import os 
from dotenv import load_dotenv
load_dotenv(override=True)

# Filepath for the cache file
CACHE_FILE = "vocabulary_cache.json"

def initialize_and_read_cache():
    """
    Ensures the cache file exists. If not, creates an empty cache file. if it does, reads the words from it.
    """
    if not os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'w') as file:
            json.dump([], file)  # Initialize with an empty list
        return {}

    else:
        with open(CACHE_FILE, 'r') as file:
            words = json.load(file)
        return words

def write_to_cache(words_list):
    """
    Adds new words to the cache file if they don't already exist.
    """
    with open(CACHE_FILE, 'r') as file:
        words = json.load(file)
  
    for word in words_list:
      if word not in words:
          words.append(word)
    
    with open(CACHE_FILE, 'w') as file:
        json.dump(words, file)

def get_categories():
    """
    get all the categories possible
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

def get_articles_with_category(category):
    """
    get the top headlines by specified category
    """
    headlines_json_response = get_headlines_response_by_category(category)
    articles_dict = get_titles_and_description_from_response(headlines_json_response)
    
    return articles_dict

def get_tool_for_function_calling():
    """
    The function returns a list of dictionaries, each representing a function that can be called.
    Each dictionary contains the function's name, description, and parameters.
    """

    cache_initializing_and_reading_function = {
        "name": "initialize_and_read_cache",
        "description": "Ensures the cache file exists. If not, creates an empty cache file. Then, it reads the cache file so the model will have access to the known words vocabulary. Call this every time the user starts a new chat session, sends you a first message etc.",
        "parameters": {
          "type": "object",
          "properties": {}
            }
          }
    
    cache_writing_function = {
        "name": "write_to_cache",
        "description": "Adds new words to the cache file if they don't already exist. Call this every time you recognize new Chinese words that are not in the cache and that are in the user prompt, chat history, or assistant or model response",
        "parameters": {
          "type": "object",
          "properties": {
            "words_list": {
              "type": "array",
              "items": {"type": "string"},
              "description": "a list of Chinese words that you used in the chat. the words inside the list are strings, and should be unique.",
            }
          },
          "required": ["words_list"]
        }
    }

    news_categories_function = {
        "name": "get_categories",
        "description": "Gets all the possible categories for the news API. Call this when you want to get the categories of the news API. You will use this function when you decide to start a lesson based on the news, probably because the user requested it.",
        "parameters": {
          "type": "object",
          "properties": {}
            }
          }
    
    articles_with_category_function = {
        "name": "get_articles_with_category",
        "description": "Gets the top headlines by specified category. Call this when you want to get the top headlines by a category chosen by the user, after you presented him the possible categories and he chose one.",
        "parameters": {
          "type": "object",
          "properties": {
            "category": {
              "type": "string",
              "description": "the category of the news API. You can get the categories by calling the get_categories function.",
            }
          },
          "required": ["category"]
        }
    }

              
    return [cache_initializing_and_reading_function, 
            cache_writing_function, 
            news_categories_function,
            articles_with_category_function]

def construct_tools_object_list():
    """
    Constructs a list of tools for function calling.
    Each tool is a dictionary containing keys: 
      1. type: function 
      2. function: the function dictionary descring it in the necessary format
    """
    tools = []
    for function_dict in get_tool_for_function_calling():
        tools.append({
            "type": "function",
            "function": function_dict
        })
    
    return tools

