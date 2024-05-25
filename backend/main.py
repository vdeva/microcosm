from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os
import psycopg2
import random
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load environment variables
load_dotenv()

# Environment variables
MISTRAL_API_TOKEN = os.getenv('MISTRAL_API_TOKEN')
DATABASE_URL = os.getenv("DATABASE_URL")
client = MistralClient(api_key=MISTRAL_API_TOKEN)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Tweet(BaseModel):
    name: str
    handle: str
    content: str
    replies: int
    likes: int

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def get_random_humans(count):
    conn = get_db_connection()
    humans = []
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, address, username FROM human ORDER BY RANDOM() LIMIT %s", (count,))
        humans = cur.fetchall()
    conn.close()
    return humans

def get_recent_news():
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT title, content FROM news_articles ORDER BY created_at DESC LIMIT 40")
        articles = cur.fetchall()
    conn.close()
    return articles

def insert_tweet(tweet: Tweet, author_id: int):
    conn = get_db_connection()
    with conn.cursor() as cur:
        # Prepare the tweet data for insertion
        tweet_data = (tweet.name, tweet.handle, tweet.content, tweet.likes, author_id)
        cur.execute("""
            INSERT INTO tweet (name, handle, content, likes, author_id)
            VALUES (%s, %s, %s, %s, %s)
        """, tweet_data)
        conn.commit()
    conn.close()

tweet_template = """
    You are the following person:
    Name: {name}
    Address: {address}
    Here are some news happening in the world:
    {news1}
    {news2}
    {news3}
    Write an extremely short post about stuff that's on your mind, it doesn't have to be about the news, although it can be.
    Don't put quotes around the post. NEVER PUT HASTAGS IN THE POST.
    ONLY REPLY THE POST. DO NOT SAY ANYTHING BESIDES THE POST.
"""

def generate_tweet(human, selected_articles):
    tweet_content = tweet_template.format(
        name=human[1],
        address=human[2],
        news1=f'{selected_articles[0][0]}: {selected_articles[0][1]}',
        news2=f'{selected_articles[1][0]}: {selected_articles[1][1]}',
        news3=f'{selected_articles[2][0]}: {selected_articles[2][1]}'
    )
    response = client.chat(
        model='mistral-large-latest',
        random_seed=random.randint(0,10000000000),
        messages=[ChatMessage(role='user', content=tweet_content)],
        temperature=1,
    )
    tweet_text = response.choices[0].message.content.strip()
    return Tweet(name=human[1], handle=human[3], content=tweet_text, replies=random.randint(0,100), likes=random.randint(0,800))

def generate_and_store_tweet(human, news_articles):
    selected_articles = random.sample(news_articles, 3)
    tweet = generate_tweet(human, selected_articles)
    insert_tweet(tweet, human[0])  # Assuming human[0] is the author's ID
    return tweet

@app.get("/twitterfeed", response_model=List[Tweet])
async def get_twitter_feed():
    num_tweets = 10
    humans = get_random_humans(num_tweets)

    if not humans or len(humans) < num_tweets:
        raise HTTPException(status_code=404, detail="Not enough humans found")

    news_articles = get_recent_news()

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(generate_and_store_tweet, human, news_articles) for human in humans]
        tweets = [future.result() for future in as_completed(futures)]

    return tweets
