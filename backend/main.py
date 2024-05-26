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
import datetime
from psycopg2.extras import Json
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import Query
import numpy as np
import os

from groq import Groq

# Load environment variables
load_dotenv()

# Environment variables
MISTRAL_API_TOKEN = os.getenv('MISTRAL_API_TOKEN')
DATABASE_URL = os.getenv("DATABASE_URL")
client = MistralClient(api_key=MISTRAL_API_TOKEN)


client2 = Groq(
    # This is the default and can be omitted
    api_key=os.environ.get("GROQ_API_TOKEN"),
)


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
    id: int

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
    try:
        with conn.cursor() as cur:
            # Generate embeddings for the tweet content
            embeddings_response = client.embeddings(
                model="mistral-embed",
                input=[tweet.content]
            )
            embedding_vector = embeddings_response.data[0].embedding  # Assuming response is successful and valid

            # Prepare the tweet data for insertion including the embedding vector
            tweet_data = (tweet.name, tweet.handle, tweet.content, tweet.likes, author_id, Json(embedding_vector))
            cur.execute("""
                INSERT INTO tweet (name, handle, content, likes, author_id, vector)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, tweet_data)
            conn.commit()
    finally:
        conn.close()

tweet_template = """
    You are the following person:
    Name: {name}
    Address: {address}
    Here are some news happening in the world:
    {news1}
    {news2}
    {news3}
    {stock_info}
    Write an extremely short post about stuff that's on your mind, it doesn't have to be about the news or stocks, although it can be.
    Don't put quotes around the post. NEVER PUT HASTAGS IN THE POST.
    ONLY REPLY THE POST. DO NOT SAY ANYTHING BESIDES THE POST.
"""

def generate_tweet(human, selected_articles, selected_stocks=None):

    if selected_stocks:
        stock_info = f'Also, check out these stock movements:\n' + '\n'.join(
            f'{stock["symbol"]}: {stock["name"]} recently traded at ${stock["price"]:.2f}' 
            for stock in selected_stocks
        )
    else:
        stock_info = ""

    tweet_content = tweet_template.format(
        name=human[1],
        address=human[2],
        news1=f'{selected_articles[0][0]}: {selected_articles[0][1]}',
        news2=f'{selected_articles[1][0]}: {selected_articles[1][1]}',
        news3=f'{selected_articles[2][0]}: {selected_articles[2][1]}',
        stock_info=stock_info
    )
    response = client.chat(
        model='mistral-large-latest',
        random_seed=random.randint(0,10000000000),
        messages=[ChatMessage(role='user', content=tweet_content)],
        temperature=1,
    )
    tweet_text = response.choices[0].message.content.strip()
    return Tweet(name=human[1], handle=human[3], content=tweet_text, replies=random.randint(0,100), likes=random.randint(0,800), id=human[0])

def get_recent_stock_prices(limit=2):
    conn = get_db_connection()
    stocks = []
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT s.symbol, s.name, sp.price
                FROM stocks s
                JOIN stock_prices sp ON s.id = sp.stock_id
                WHERE sp.timestamp = (
                    SELECT MAX(sp2.timestamp)
                    FROM stock_prices sp2
                    WHERE sp2.stock_id = s.id
                )
                ORDER BY RANDOM()
                LIMIT %s
            """, (limit,))
            stocks = [{'symbol': row[0], 'name': row[1], 'price': row[2]} for row in cur.fetchall()]
    finally:
        conn.close()
    return stocks

def generate_and_store_tweet(human, news_articles):
    stocks_data = get_recent_stock_prices(2)
    selected_articles = random.sample(news_articles, 3)
    include_stocks = random.choice([True, False])
    selected_stocks = random.sample(stocks_data, 2) if include_stocks and stocks_data else None
    tweet = generate_tweet(human, selected_articles, selected_stocks)
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

class Article(BaseModel):
    title: str
    content: str

def get_recent_articles():
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT title, content FROM news_articles ORDER BY created_at DESC LIMIT 40")
        articles = cur.fetchall()
    conn.close()
    return [Article(title=title, content=content) for title, content in articles]

@app.get("/recent-articles", response_model=List[Article])
async def recent_articles():
    articles = get_recent_articles()
    return articles

class Wikipage(BaseModel):
    title: str
    content: str

def get_recent_wikipages():
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT title, content FROM wikipages ORDER BY created_at DESC LIMIT 40")
        wikipages = cur.fetchall()
    conn.close()
    return [Wikipage(title=title, content=content) for title, content in wikipages]

@app.get("/recent-wikipages", response_model=List[Wikipage])
async def recent_wikipages():
    wikipages = get_recent_wikipages()
    return wikipages

class StockPrice(BaseModel):
    price: float
    timestamp: datetime.datetime

class Stock(BaseModel):
    symbol: str
    name: str
    prices: List[StockPrice]

def get_stocks_with_prices():
    conn = get_db_connection()
    stocks = []
    with conn.cursor() as cur:
        cur.execute("""
            SELECT s.id, s.symbol, s.name, sp.price, sp.timestamp
            FROM stocks s
            JOIN stock_prices sp ON s.id = sp.stock_id
            WHERE sp.id IN (
                SELECT sp2.id
                FROM stock_prices sp2
                WHERE sp2.stock_id = s.id
                ORDER BY sp2.timestamp DESC
                LIMIT 20
            )
            ORDER BY s.symbol, sp.timestamp DESC
        """)
        raw_data = cur.fetchall()

    # Organizing the data into a dictionary grouped by stock symbol
    stocks_dict = {}
    for stock_id, symbol, name, price, timestamp in raw_data:
        if symbol not in stocks_dict:
            stocks_dict[symbol] = {
                'symbol': symbol,
                'name': name,
                'prices': []
            }
        stocks_dict[symbol]['prices'].append({'price': price, 'timestamp': timestamp})

    # Convert the dictionary to a list of Stock models
    for symbol, stock_data in stocks_dict.items():
        stock = Stock(
            symbol=stock_data['symbol'],
            name=stock_data['name'],
            prices=[StockPrice(**price) for price in stock_data['prices']]
        )
        stocks.append(stock)

    conn.close()
    return stocks

@app.get("/stocks", response_model=List[Stock])
async def get_stocks():
    stocks = get_stocks_with_prices()
    return stocks


def insert_wikipage(title: str, content: str):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO wikipages (title, content, created_at)
                VALUES (%s, %s, %s)
            """, (title, content, datetime.datetime.now()))
            conn.commit()
    finally:
        conn.close()


class WikiQuery(BaseModel):
    query: str

@app.get("/generate-wiki", response_model=Wikipage)
async def generate_wiki(query: str = Query(..., description="Search query to generate wiki content")):
    conn = get_db_connection()
    search_vector = client.embeddings(
        model="mistral-embed",
        input=[query]
    ).data[0].embedding  # Assume successful response
    
    # Fetch tweets and compute similarity
    with conn.cursor() as cur:
        cur.execute("SELECT id, content, vector FROM tweet")
        tweets = cur.fetchall()
    
    # Calculate cosine similarity
    similarities = []
    for tweet in tweets:
        tweet_vector = np.array(tweet[2])
        sim = cosine_similarity([search_vector], [tweet_vector])[0][0]
        similarities.append((tweet[0], tweet[1], sim))
    
    # Sort by similarity and pick top 5
    top_tweets = sorted(similarities, key=lambda x: x[2], reverse=True)[:5]
    tweets_content = " ".join(tweet[1] for tweet in top_tweets)

    print(tweets_content);
    
    # Generate wiki content
    wiki_template = f"""
    Search query: {query}
    Related Posts: {tweets_content}
    Write a comprehensive wiki entry about {query}, including relevant details and insights.
    Include an infobox.
    Only return the body of the article in wikitext format. Nothing else.
    """
    
    wiki_response = client2.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": wiki_template}
        ],
        temperature=0.7,
    )
    wiki_content = wiki_response.choices[0].message.content.strip()
    insert_wikipage(query, wiki_content)
    
    conn.close()
    return Wikipage(title=f"{query}", content=wiki_content)