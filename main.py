import asyncio
from stream_gpt_mcp import stream_gpt_mcp
from introduced_vocabulary_and_tools_handling.tools_mcp import tools_sse_client


async def chat_session():
    """
    Creates a chat session where the chat history is preserved.
    Allows the user to interact with the chatbot in a session-like manner.
    """

    # initialize the mcp server and client to have access to the tools
    client = await tools_sse_client.initialize_mcp_server_and_client()
    
    # Wait for the server to start
    # await asyncio.sleep(2)

    chat_history = []  # Initialize an empty chat history
    print("Chat session started. Type 'exit' to end the session.\n")

    while True:

        prompt = input("You: ")
        if prompt.lower() == "exit":
            print("Chat session ended.")
            break


        result = stream_gpt_mcp(client, prompt, chat_history)
        print("Bot:", end=" ")
        async for item in result:  
            print(item, end="", flush=True)
        print("\n")

if __name__ == "__main__":
    # Start the chat session with the system prompt
    asyncio.run(chat_session())