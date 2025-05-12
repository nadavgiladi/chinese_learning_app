# Chinese Learning App

This project is a chatbot-based Chinese learning application designed to help English speakers learn Chinese vocabulary and practice conversational skills. The chatbot uses OpenAI's GPT model to provide interactive lessons, vocabulary management, and real-time feedback.

## Features

- **Interactive Chatbot**: Engage in conversations with a chatbot acting as a Chinese teacher.
- **Vocabulary Management**: Automatically tracks and manages your learned vocabulary in a vocabulary file to preserve progress.
- **Vocabulary Management**: Supports tool calls for reading and writing vocabulary to the cache.
- **News and Linkedin Based Lessons**: You can ask the teacher to base the lesson on the latest news, or to learn introducing yourself based on your Linkedin profile.


## Prerequisites

- Python 3.10+
- Node.js 18+ (must include npm and npx) -> for macos: install by executing in the terminal ```brew install node```
- uv -> for macos: execute in the terminal ```curl -LsSf https://astral.sh/uv/install.sh | sh```

## Getting Started
1. **Install Dependecies**: on your terminal go to the project path and run: ```pip install -r requirements.txt```
2. **Set Up Environment Variables**: Create a .env file inside the project's main folder and add your:
  OpenAI API key: ```OPENAI_API_KEY=your_openai_api_key```
  News API key: ```NEWS_API_KEY=your_news_api_key```
  Rapid API key for ```fresh-linkedin-profile-data```: ```RAPIDAPI_KEY=2281f1e2bdmsh002721f6906ab46p1ea867jsn903210fe8cc2```
  (Go to rapidapi.com -> search for fresh-linkedin-profile-data -> register for the free tier and get your key)

3. **Run the App**: ```python3 main.py```



