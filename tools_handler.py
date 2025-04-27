from introduced_vocabulary_handling.cache_handler import *

def handle_tool_calls(final_tool_calls_request_dict):
    """
    Handles the tool calls by executing the functions and returning the results.
    """
    tool_messages = []

    for tool_call_req_index, tool_call_req_val in final_tool_calls_request_dict.items():
        # extract the function name
        function_name_to_call = tool_call_req_val.function.name
        
        if function_name_to_call == 'write_to_cache':
            arguments = json.loads(tool_call_req_val.function.arguments)
            words_list = arguments.get('words_list')
            write_to_cache(words_list)
            tool_message = {
                "role": "tool",
                "content": f"The words {words_list} were written to the cache",
                "tool_call_id": tool_call_req_val.id
            }
        elif function_name_to_call == 'initialize_and_read_cache':
            known_words_dict = initialize_and_read_cache()
            tool_message = {
                "role": "tool",
                "content": json.dumps({"words_list": known_words_dict}),
                "tool_call_id": tool_call_req_val.id
            }
        
        elif function_name_to_call == 'get_categories':
            print("get_categories function called")
            categories_list = get_categories()
            tool_message = {
                "role": "tool",
                "content": json.dumps({"categories_list": categories_list}),
                "tool_call_id": tool_call_req_val.id
            }
        
        elif function_name_to_call == 'get_articles_with_category':
            print("get_articles_with_category function called")
            arguments = json.loads(tool_call_req_val.function.arguments)
            category = arguments.get('category')
            articles_dict = get_articles_with_category(category)
            tool_message = {
                "role": "tool",
                "content": json.dumps({"articles_dict": articles_dict}),
                "tool_call_id": tool_call_req_val.id
            }
            
        else:
            print(f"Error: a function to be called: {function_name_to_call} isn't mapped to a function handling method in handle_tool_call")

        tool_messages.append(tool_message)
    return tool_messages