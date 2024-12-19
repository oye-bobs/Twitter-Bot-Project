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
    "Energy fact: Wind power",
    "Energy fact: Renewable energy",
    "Energy fact: Clean energy",
    "Energy fact: Sustainable energy"
]

def generate_fact():
    """Generate a fact using GPT-2"""
    try:
        # Get a random prompt
        prompt = random.choice(prompts)
        print(f"Using prompt: {prompt}")
        
        # Generate text with explicit truncation
        result = generator(
            prompt, 
            max_length=200, 
            num_return_sequences=1,
            temperature=0.7,
            truncation=True  # Explicitly set truncation
        )[0]['generated_text']
        
        return result
    except Exception as e:
        print(f"Error generating fact: {e}")
        return None

def split_into_tweets(text, max_length=280):
    """Split text into a list of tweets, each within the max_length"""
    words = text.split()
    tweets = []
    current_tweet = ""

    for word in words:
        if len(current_tweet) + len(word) + 1 > max_length:
            tweets.append(current_tweet)
            current_tweet = word
        else:
            if current_tweet:
                current_tweet += " " + word
            else:
                current_tweet = word

    if current_tweet:
        tweets.append(current_tweet)

    return tweets

def post_tweet_thread():
    """Post a thread of tweets with error handling"""
    tweet_content = generate_fact()
    if tweet_content:
        tweets = split_into_tweets(tweet_content)
        try:
            # Post the first tweet
            response = client.create_tweet(text=tweets[0])
            tweet_id = response.data["id"]
            
            # Post the rest of the tweets as replies to the first tweet
            for tweet in tweets[1:]:
                response = client.create_tweet(text=tweet, in_reply_to_tweet_id=tweet_id)
                tweet_id = response.data["id"]
            
            print("\n✅ Thread posted successfully:")
            print("-" * 50)
            for tweet in tweets:
                print(tweet)
            print("-" * 50)
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
            post_tweet_thread()
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