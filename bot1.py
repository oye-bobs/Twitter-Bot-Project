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

# Initialize the BART model for text summarization
summarizer = pipeline('summarization', model='facebook/bart-large-cnn')

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

def summarize_text(text, max_length=280):
    """Summarize text to meet Twitter's character limit"""
    if len(text) <= max_length:
        return text
    try:
        summary = summarizer(text, max_length=int(max_length * 0.8), min_length=50, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return text[:max_length]

def post_tweet():
    """Post a tweet with error handling and summarization"""
    tweet_content = generate_fact()
    if tweet_content:
        summarized_content = summarize_text(tweet_content)
        try:
            response = client.create_tweet(text=summarized_content)
            if response.data:
                print("\n✅ Tweet posted successfully:")
                print("-" * 50)
                print(summarized_content)
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