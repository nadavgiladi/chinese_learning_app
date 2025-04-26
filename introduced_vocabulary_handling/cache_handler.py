import json
import os


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
    
    return [cache_initializing_and_reading_function, cache_writing_function]

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

