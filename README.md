# Translation Bot

This project is a translation bot that translates text between Chinese and Indonesian using an LLM managed by OpenAI. The bot receives input in one language and outputs the translation in the other language.

## Project Structure

```sh
translation-bot
├── src
│   ├── main.py                # Main entry point of the application
│   ├── services
│   │   ├── line_service.py     # Handles interactions with LINE API
│   └── utils
│       └── helper.py # Contains utility functions for translation
├── docker
│   ├── docker-compose.yaml     # Docker Compose configuration
│   ├── dockerfile              # Dockerfile for building the image
│   └── requirements.txt        # Python dependencies for the Docker image
├── .env.example                       # Environment variables for sensitive information
├── .gitignore
├── requirements.txt           # Python dependencies for the project
└── README.md                  # Project documentation
```

## Installation

1. Clone the repository:

   ```sh
   git clone <repository-url>
   cd translation-bot
   ```

2. Set up your environment variables in the `.env` file. You will need to include:
   - PORT
   - OPENAI_API_KEY
   - LINE Channel Secret and Access Token
   - LINE_USER_ID                          # set this variable to the user ID of the target user receiving the translation

## Usage

To run the translation bot, execute the following command:

```sh
cd docker
docker-compose --env-file=../.env up
```

To stop the translation bot, execute the following command:

```sh
cd docker
docker-compose --env-file=../.env up
```

The bot will listen for user input and translate between Chinese and Indonesian based on the input language.
