# Chinese Learning App

This project is a chatbot-based Chinese learning application designed to help English speakers learn Chinese vocabulary and practice conversational skills. The chatbot uses OpenAI's GPT model to provide interactive lessons, vocabulary management, and real-time feedback.

## Features

- **Interactive Chatbot**: Engage in conversations with a chatbot acting as a Chinese teacher.
- **Vocabulary Management**: Automatically tracks and manages your learned vocabulary in a vocabulary file to preserve progress.
- **Tool Integration**: Supports tool calls for reading and writing vocabulary to the cache.


## Project Structure

### main.py 
Entry point for the chatbot application 

### stream_gpt.py
Handles GPT-based streaming responses 

### cache_handler.py
Manages vocabulary cache operations 

### introduced_vocabulary_handling.cache_handler.py
Vocabulary handling utilities

### vocabulary_cache.json
Stores the user's vocabulary

### requirements.txt
Python dependencies

## Getting Started
1. **Install Dependecies**: on your terminal go to the project path and run: ```pip install -r requirements.txt```
2. **Set Up Environment Variables**: Create a .env file inside the project's main folder and add your OpenAI API key: ```OPENAI_API_KEY='your_openai_api_key'```
3. **Run the App**: ```python3 main.py```



