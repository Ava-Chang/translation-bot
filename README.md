# Translation Bot

This project is a translation bot that translates text between Chinese and Indonesian using an LLM managed by OpenAI. The bot receives input in one language and outputs the translation in the other language.

## Project Structure

```sh
translation-bot
├── src
│   ├── __init__.py
│   ├── main.py                # Main entry point of the application
│   ├── services
│   │   ├── __init__.py
│   │   └── line_service.py    # Handles interactions with LINE API
│   └── utils
│       ├── __init__.py
│       └── helper.py          # Contains utility functions for translation
├── docker
│   ├── docker-compose.yaml    # Docker Compose configuration
│   ├── dockerfile            # Dockerfile for building the image
│   └── requirements.txt      # Python dependencies for the Docker image
├── .env.example             
├── .gitignore
├── requirements.txt         # Python dependencies for the vercel project deploy
├── setup.cfg               # Python package configuration
├── vercel.json            # Vercel deployment configuration
└── README.md              # Project documentation

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/Ava-Chang/translation-bot.git
   cd translation-bot
   ```

2. copy the `.env.example` file to `.env`:

   ```sh
   cp .env.example .env
   ```

3. Set up your environment variables in the `.env` file. You will need to include:
   - PORT                                  # Port for the application to run on
   - FLASK_ENV                             # default "development"
   - OPENAI_API_KEY                        # OpenAI API key for LLM
   - LINE Channel Secret and Access Token
   - LINE_GROUP_ID                         # setting the group id for the bot to respond

## Usage

To run the translation bot, execute the following command:

```sh
cd docker
docker-compose --env-file=../.env up
```

To stop the translation bot, execute the following command:

```sh
cd docker
docker-compose --env-file=../.env down
```

The bot will listen for user input and translate between Chinese and Indonesian based on the input language.
