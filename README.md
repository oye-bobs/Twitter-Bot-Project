# Twitter-Bot-Project
Twitter Energy Facts Bot This repository contains Two Twitter bots that posts interesting and informative energy facts at regular intervals. The bot1 uses the GPT-2 model from Hugging Face's transformers library to generate unique content and the Tweepy library to interact with the Twitter API.
While bot randomly selects from already provided facts and posts on twitter at schedules times.
# Twitter Energy Facts Bot

This repository contains a Twitter bot that posts interesting and informative energy facts at regular intervals. The bot uses the GPT-2 model from Hugging Face's transformers library to generate unique content and the Tweepy library to interact with the Twitter API.

## Features

- **Automated Tweeting**: Posts tweets at predefined intervals without manual intervention.
- **AI-Generated Content**: Uses GPT-2 to generate informative energy facts.
- **Easy Configuration**: Simple setup with environment variables for Twitter API credentials.
- **Error Handling**: Robust error handling and retry mechanisms to ensure reliable operation.

## Technologies Used

- **Python**: The main programming language for the bot.
- **Hugging Face Transformers**: For GPT-2 text generation.
- **Tweepy**: For interacting with the Twitter API.
- **Dotenv**: For managing environment variables.

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/twitter-energy-facts-bot.git
   cd twitter-energy-facts-bot


## Steps

i. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

ii. Install the required packages: 
```bash 
pip install -r requirements.txt

iii. Create a .env file in the root of the project and add your Twitter API credentials:
```eni
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET_KEY=your_api_secret_key
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret


## Usage

To start the bot, run:
```bash
python bot.py
python bot1.py


##Contributing

Contributions are welcome! Please open an issue or submit a pull request.

-Fork the repository
-Create a new branch (git checkout -b feature-branch)
-Commit your changes (git commit -m 'Add new feature')
-Push to the branch (git push origin feature-branch)
-Open a pull request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

