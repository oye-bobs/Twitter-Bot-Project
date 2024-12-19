import tweepy
from transformers import pipeline
from dotenv import load_dotenv
import os
import time
import random

# Load environment variables from .env file
load_dotenv()

# Set up Twitter API v2 credentials
client = tweepy.Client(
    consumer_key=os.getenv('TWITTER_API_KEY'),
    consumer_secret=os.getenv('TWITTER_API_SECRET_KEY'),
    access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
)

# Initialize the GPT-2 model for text generation
generator = pipeline('text-generation', model='gpt2')

# Predefined prompts for energy facts
prompts = [
    "Energy fact about Solar energy summarised in 150 words ",
  
    #"Energy fact: Wind power",
    #"Energy fact: Renewable energy",
    #"Energy fact: Clean energy",
    #"Energy fact: Sustainable energy" 
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
            max_length=300, 
            num_return_sequences=1,
            temperature=0.7,
            truncation=True  # Explicitly set truncation
        )[0]['generated_text']
        
        # Clean up the generated text
        fact = result.split('\n')[0]  # Take only the first line
        return fact
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

def post_tweet():
    """Post a tweet or a thread of tweets with error handling"""
    tweet_content = generate_fact()
    if tweet_content:
        if len(tweet_content) <= 280:
            # Post a single tweet if within character limit
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
                if e.response.status_code == 429:
                    print(f"❌ Twitter API Error: {e} - Rate limit exceeded. Waiting for 15 minutes before retrying.")
                    time.sleep(900)  # Wait for 15 minutes
                else:
                    print(f"❌ Twitter API Error: {e}")
        else:
            # Split and post as a thread if exceeds character limit
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
                if e.response.status_code == 429:
                    print(f"❌ Twitter API Error: {e} - Rate limit exceeded. Waiting for 15 minutes before retrying.")
                    time.sleep(900)  # Wait for 15 minutes
                else:
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