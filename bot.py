import tweepy
from dotenv import load_dotenv
import os
import time
from datetime import datetime, timezone
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

# Configuration
INTERVAL = 900  # 15 minutes in seconds

# Predefined facts
facts = [
    "Solar panels can still generate electricity on cloudy days, though less efficiently than in direct sunlight.",
    "Wind energy is one of the fastest-growing renewable energy sources worldwide.",
    "The Earth's average temperature has increased by about 1.1°C since the pre-industrial era.",
    "Solar energy is the most abundant energy source on Earth—173,000 terawatts strikes the Earth continuously.",
    "A single wind turbine can power hundreds of homes.",
    "The solar industry creates jobs 17 times faster than the rest of the US economy.",
    "Renewable energy sources now account for about 26% of global electricity generation.",
    "The cost of solar panels has dropped by more than 80% since 2010.",
    "Electric vehicles produce zero direct emissions, helping reduce air pollution in cities.",
    "Geothermal energy comes from the Earth's core, which is as hot as the sun's surface.",
    "Ocean waves could supply twice the amount of electricity the world produces now.",
    "The Sahara Desert receives enough sunlight to power the entire world through solar energy.",
    "Renewable energy jobs worldwide reached 11.5 million in 2019.",
    "The first solar cell was created in 1954 by Bell Labs.",
    "Some countries, like Iceland, get nearly all their electricity from renewable sources."
]

def format_fact(fact):
    """Format the fact with 'Energy Fact:' prefix"""
    return f"Energy Fact: {fact}"

def get_fact():
    """Get a random formatted fact"""
    try:
        return format_fact(random.choice(facts))
    except Exception as e:
        print(f"Error generating fact: {e}")
        return None

def post_tweet():
    """Post a tweet with error handling"""
    tweet_content = get_fact()
    if tweet_content:
        try:
            # Using Twitter API v2 endpoint
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
    print(f"⏱️ Posting interval: {INTERVAL} seconds (15 minutes)")
    print("-" * 50)

    while True:
        try:
            post_tweet()
            print("\n⏭️ Next tweet in 15 minutes...")
            time.sleep(INTERVAL)

        except KeyboardInterrupt:
            print("\n🛑 Bot stopped by user")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            print("⏳ Waiting 60 seconds before retrying...")
            time.sleep(60)

if __name__ == "__main__":
    main()