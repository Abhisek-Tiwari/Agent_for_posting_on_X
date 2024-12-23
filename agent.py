# Import important libraries
import openai
import tweepy
import random
import datetime

# OpenAI API Key
OPENAI_API_KEY = "openai_api_key"

# Twitter API Keys
TWITTER_API_KEY = "twitter_api_key"
TWITTER_API_SECRET = "twitter_api_secret"
TWITTER_ACCESS_TOKEN = "twitter_access_token"
TWITTER_ACCESS_SECRET = "twitter_access_secret"

# Set up OpenAI
openai.api_key = OPENAI_API_KEY

# Set up authentication and API
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
twitter_api = tweepy.API(auth)

# Fetch trending topics by this function
def fetch_trending_topics():
    """
    Summary:
    We use the twitter api to fetch top 10 trending topics world wide

    Returns:
        List: List of trending topics
    """
    try:
        trends = twitter_api.get_place_trends(id=1)  # WOEID 1 is for global trends
        trending_topics = [trend["name"] for trend in trends[0]["trends"][:10]]
        return trending_topics
    except Exception as e:
        print(f"Error fetching trends: {e}")
        return ["AI", "Tech", "Innovation"]  # Default topics


# Here's a quick analysis of the ideas given by the following agents:
# aixbt_agent : coins, finance, market, AI agents
# vader_ai_ : coin's price increase/decrease %, crypto
# tri_sigma_ : Trading, Finance, Coins, AIs, crypto
# 0x_Loky : meme coin/vistual prices, Web3


# Prompt Generator
def generate_prompt(agent_style, topic, dynamic_elements):
    """ 
    Summary:
        We generate the prompt to be fed to openai or to generate tweet for the agent to post on twitter
    Args:
        agent_style (string): The agent on twitter who we want to imitate
        topic (string): The trending topic we want to post about
        dynamic_elements (string): The trending topics we want to include in the tweet

    Returns:
        string: The prompt to be fed to openai
    """
    templates = {
        "aixbt_agent": "Write real-time Twitter updates on '{topic}' focusing on cryptocurrency price movements for an agent similar to @aixbt_agent. The tweets should highlight significant token metrics like market cap, price changes (percentage and direction), and trading volume. Maintain a concise, engaging tone suitable for crypto traders, and include actionable observations or insights. Format the tweets to provide immediate clarity, and emphasize real-time relevance.",
        "Vader_AI_": "Write a concise update on '{topic}' and related trends ({trends}) with respect to cryptocurrency price movements, focusing on tokens with significant hourly changes. Highlight abnormal returns using percentages and emojis (📈 for increases, 📉 for decreases).",
        "tri_sigma_": "Write a Twitter thread analyzing '{topic}' and related trends ({trends}) with respect to Crypto, finance, and AI. Start with a catchy title that questions its potential...",
        "0x_Loky": "Write a real-time Twitter update about cryptocurrency price movements related to '{topic}' and trends ({trends}). Categorize tokens by theme..."
    }
    template = templates.get(agent_style, templates["aixbt_agent"]) # Default to aixbt_agent if agent_style is not found
    # Join dynamic elements into a comma-separated string
    trends = ", ".join(dynamic_elements)
    return template.format(topic=topic, trends=trends)

# Generate tweet by this function
def generate_tweet(agent_style, topic, dynamic_elements):
    """
    Summary:
        We generate the tweet by feeding the prompt to openai
    Args:
        agent_style (string): The agent on twitter who we want to imitate
        topic (string): The trending topic we want to post about
        dynamic_elements (string): The trending topics we want to include in the tweet

    Returns:
        string: The tweet to be posted on twitter
    """
    prompt = generate_prompt(agent_style, topic, dynamic_elements)
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=280,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error generating tweet: {e}")
        return "AI is amazing. Let's innovate together! #AI #Tech"


# Post Tweet by this function
def post_tweet(content):
    """
    Summary:
        This function schedules the tweet to be posted on twitter/ posts the tweet
    Args:
        content (string): The tweet to be posted on twitter
    """
    try:
        twitter_api.update_status(content)
        print(f"Tweet posted: {content}")
    except Exception as e:
        print(f"Error posting tweet: {e}")


# Main function to implement the workflow
def main():
    agents = ["aixbt_agent", "Vader_AI_", "tri_sigma_", "0x_Loky"]
    trending_topics = fetch_trending_topics()

    for agent in agents:
        topic = random.choice(trending_topics)
        tweet = generate_tweet(agent, topic, trending_topics)
        print(f"Generated tweet for {agent}: {tweet}")
        post_tweet(tweet)

if __name__ == "__main__":
    main()
