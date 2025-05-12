import os
from dotenv import load_dotenv
from openai import OpenAI
from introduced_vocabulary_and_tools_handling.tools_handler_mcp import handle_tool_calls
from model_configs import ModelConfig
from introduced_vocabulary_and_tools_handling.tools_mcp import tools_sse_client



async def stream_gpt_mcp(client, prompt, chat_history):
    """
    Stream the response from the OpenAI API using a configured model version. Including tool calls handling and chat history management. 
    """

    # load configured model name and system message
    model_configs = ModelConfig()
    model_version = model_configs.model_name
    system_message = model_configs.system_message

    load_dotenv(override=True)
    openai_api_key = os.getenv('OPENAI_API_KEY')
    openai = OpenAI()
    model_name = model_version
    
    # construct the tools objects list as expected by OpenAI
    tools_object_list = await tools_sse_client.list_tools(client)

    # Add system message and chat history to the messages list
    messages = [{"role": "system", "content": system_message}] + chat_history
    messages.append({"role": "user", "content": prompt})
    chat_history.append({"role": "user", "content": prompt})

    stream = openai.chat.completions.create(
        model=model_name,
        messages=messages,
        tools=tools_object_list,
        stream=True
    )

    # add the current prompt and full response to the session history, and yield the response
    full_response_text = ""
    final_tool_calls_request_dict = {}
    tool_calls_list = []
    for chunk in stream:
        
        # start handling tool calls by aggregating tool_calls response up to the finish_reason == tool_call
        for tool_call in chunk.choices[0].delta.tool_calls or []:
            index = tool_call.index
            if index not in final_tool_calls_request_dict:
                final_tool_calls_request_dict[index] = tool_call
                tool_calls_list.append(tool_call)
            final_tool_calls_request_dict[index].function.arguments += tool_call.function.arguments
        
        
        # get the content text from each chunk
        chunk_text = chunk.choices[0].delta.content
        
        # add the chunk content to the full response 
        full_response_text += chunk_text or ""

        # check if a finish_reason of tool call has occurred -> start the tool calling process
        if chunk.choices[0].finish_reason == 'tool_calls':
            
            # append to the messages the tool_calls request
            messages.append({"role":"assistant", "content": None, "tool_calls": tool_calls_list})
            chat_history.append({"role":"assistant", "content": None, "tool_calls": tool_calls_list})

            # construct the tool_messages messages
            tool_messages = await handle_tool_calls(client, final_tool_calls_request_dict)

            # add each tool message to the messages
            for tool_message in tool_messages:
                messages.append(tool_message)
                chat_history.append(tool_message)

            # create an additional response with the new messages that includes both tool request messages and tools response messages
            stream = openai.chat.completions.create(
                model=model_name,
                messages=messages,
                stream=True)
            
            for chunk in stream:
                chunk_text = chunk.choices[0].delta.content
                full_response_text += chunk_text or ""
                yield chunk_text or ""

            
        yield chunk_text or ""
    
    messages.append({"role": "assistant", "content": full_response_text})
    chat_history.append({"role": "assistant", "content": full_response_text})

