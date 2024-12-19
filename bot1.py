import tweepy
from transformers import pipeline
from dotenv import load_dotenv
import os
import time
from datetime import datetime, timezone
import random  # Ensure this import is included

# Load environment variables from .env file
load_dotenv()

# Set up Twitter API v2 credentials
client = tweepy.Client(
    consumer_key=os.getenv('TWITTER_API_KEY'),
    consumer_secret=os.getenv('TWITTER_API_SECRET_KEY'),
    access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
)

# Initialize the GPT-2 model
generator = pipeline('text-generation', model='gpt2')

# Predefined prompts for energy facts
prompts = [
    "Energy fact: Solar energy",
    "Energy fact: Solar Inverters",
    "Energy fact: Renewable energy",
    "Energy fact: Clean energy",
    "Energy fact: Sustainable energy",
    "Energy fact: Solar Batteries",
    "Energy fact: Renewable Energy in Africa",
    "Energy fact: Global warming"
]

def generate_fact():
    """Generate a fact using GPT-2"""
    try:
        # Get a random prompt
        prompt = random.choice(prompts)
        print(f"Using prompt: {prompt}")
        
        # Generate text
        result = generator(
            prompt, 
            max_length=100, 
            num_return_sequences=1,
            temperature=0.7,
            truncation=True 
        )[0]['generated_text']
        
        # Clean up the generated text
        fact = result.split('\n')[0]  # Take only the first line
        if len(fact) > 280:  # Twitter character limit
            fact = fact[:277] + "..."
            
        return fact
    except Exception as e:
        print(f"Error generating fact: {e}")
        return None

def post_tweet():
    """Post a tweet with error handling"""
    tweet_content = generate_fact()
    if tweet_content:
        try:
            response = client.create_tweet(text=tweet_content)
            if response.data:
                print("\n✅ Tweet posted successfully:")
                print("-" * 50)
                print(tweet_content)
                print("-" * 50)
            else:
                print("❌ No response data received from Twitter")
        except tweepy.TweepyException as e:
            print(f"❌ Twitter API Error: {e}")
    else:
        print("❌ Could not generate tweet content")

def main():
    """Main function to run the bot"""
    print(f"🤖 Bot Started")
    print(f"⏱️ Using GPT-2 for text generation")
    print("-" * 50)

    while True:
        try:
            post_tweet()
            print("\n⏭️ Next tweet in 15 minutes...")
            time.sleep(900)  # 15 minutes

        except KeyboardInterrupt:
            print("\n🛑 Bot stopped by user")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            print("⏳ Waiting 60 seconds before retrying...")
            time.sleep(60)

if __name__ == "__main__":
    main()