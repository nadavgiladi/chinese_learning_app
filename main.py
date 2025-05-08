from stream_gpt import stream_gpt

def chat_session():
    """
    Creates a chat session where the chat history is preserved.
    Allows the user to interact with the chatbot in a session-like manner.
    """

    chat_history = []  # Initialize an empty chat history
    print("Chat session started. Type 'exit' to end the session.\n")

    while True:

        prompt = input("You: ")
        if prompt.lower() == "exit":
            print("Chat session ended.")
            break


        result = stream_gpt(prompt, chat_history)
        print("Bot:", end=" ")
        for item in result:  
            print(item, end="", flush=True)
        print("\n")

if __name__ == "__main__":
    # Start the chat session with the system prompt
    chat_session()