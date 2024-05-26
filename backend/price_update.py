import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import os
import numpy as np
import time
from groq import Groq

# Load environment variables
load_dotenv()

# Database and API settings
DATABASE_URL = os.getenv("DATABASE_URL")
GROQ_API_TOKEN = os.getenv("GROQ_API_TOKEN")

# Initialize Groq client for sentiment analysis
client = Groq(api_key=GROQ_API_TOKEN)

def get_recent_tweets(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT content
        FROM tweet
        ORDER BY created_at DESC
        LIMIT 40
    """)
    tweets = cur.fetchall()
    cur.close()
    return [tweet[0] for tweet in tweets]

def analyze_sentiment(tweets):
    responses = []
    for tweet in tweets:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "you are a sentiment analysis assistant. Does the person feel positive in the tweet? Only answer 'positive' or 'negative'. Nothing else."},
                {"role": "user", "content": tweet},
            ],
            model="mixtral-8x7b-32768",
        )
        responses.append(chat_completion.choices[0].message.content)
    return responses

def update_stock_prices(conn, tweets):
    cur = conn.cursor()
    
    # Analyze sentiment of recent tweets
    sentiments = analyze_sentiment(tweets)

    # Retrieve all stock IDs and names
    cur.execute("""
        SELECT id, name
        FROM stocks
    """)
    stocks = cur.fetchall()

    updates = []
    for stock_id, stock_name in stocks:
        # Check if stock name is mentioned in tweets
        mentioned = any(stock_name.lower() in tweet.lower() for tweet in tweets)
        if mentioned:
            # Determine overall sentiment towards the stock
            sentiment_score = sum('positive' in sentiment.lower() for sentiment in sentiments) - sum('negative' in sentiment.lower() for sentiment in sentiments)
            current_price_query = cur.execute("""
                SELECT COALESCE(MAX(price), 100.00)
                FROM stock_prices
                WHERE stock_id = %s
            """, (stock_id,))
            current_price = cur.fetchone()[0]
            
            # Adjust price based on sentiment
            if sentiment_score > 0:
                random_nudge = np.random.uniform(0.01, 1.00)  # Positive adjustment
            else:
                random_nudge = np.random.uniform(-1.00, -0.01)  # Negative adjustment
            
            new_price = max(0, current_price + random_nudge)
            updates.append((stock_id, new_price))

    # Insert new prices into stock_prices table
    execute_values(cur, """
        INSERT INTO stock_prices (stock_id, price)
        VALUES %s
    """, updates)
    
    conn.commit()
    cur.close()

def main():
    conn = psycopg2.connect(DATABASE_URL)
    
    try:
        while True:
            tweets = get_recent_tweets(conn)
            update_stock_prices(conn, tweets)
            print("Stock prices updated based on recent tweet sentiments.")
            time.sleep(600)  # Wait for 10 minutes before next update
    except KeyboardInterrupt:
        print("Stopped updating prices.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
