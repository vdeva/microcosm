import os
import time
import psycopg2
from dotenv import load_dotenv
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from random import randint, sample

# Load environment variables
load_dotenv()

# Database and API settings
DATABASE_URL = os.getenv("DATABASE_URL")
MISTRAL_API_TOKEN = os.getenv("MISTRAL_API_TOKEN")
client = MistralClient(api_key=MISTRAL_API_TOKEN)

def get_db_connection():
    """ Establishes a database connection """
    return psycopg2.connect(DATABASE_URL)

def get_recent_titles(limit=10):
    """ Fetches the titles of the most recent articles from the database """
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT title FROM news_articles ORDER BY id DESC LIMIT %s", (limit,))
        titles = [row[0] for row in cur.fetchall()]
    conn.close()
    return titles

def clean_title(title):
    """ Cleans the title by removing 'Title:' prefix and surrounding quotes """
    if title.lower().startswith("title:"):
        title = title[len("title:"):].strip()
    if title.startswith('"') and title.endswith('"'):
        title = title[1:-1].strip()
    return title

def generate_news_article(recent_titles):
    """ Generates a news article using the Mistral API with a check for recent titles """
    prompt = (
        "Generate a title and content for a news article. The events can range from extremely serious and sensitive topics to lighthearted stuff. "
        "Here are some recent article titles: " + "; ".join(recent_titles) + 
        ". Ensure the article you generate isn't similar to these titles. Make the topics and format very different. The title goes on the first line."
        "Do not write anything besides the title and article contents."
    )
    
    response = client.chat(
        model='mistral-large-latest',
        random_seed=randint(0, 1000000000000),
        messages=[ChatMessage(
            role='user',
            content=prompt
        )],
        temperature=1,
    )
    # Navigate through the response to get to the content
    content = response.choices[0].message.content
    title, *content_lines = content.split('\n', 1)  # Split at the first newline
    cleaned_title = clean_title(title.strip())
    return cleaned_title, ''.join(content_lines)  # Return the cleaned title and the remaining content as a single string

def insert_news_article(title, content):
    """ Inserts the generated news article into the database """
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO news_articles (title, content, importance) VALUES (%s, %s, %s)",
            (title, content, 1)  # Setting a default importance level of 1
        )
        conn.commit()
    conn.close()

def schedule_news_generation():
    """ Schedules the news article generation every 30 seconds """
    try:
        while True:
            recent_titles = get_recent_titles()
            title, content = generate_news_article(recent_titles)
            insert_news_article(title, content.strip())
            print(f"Inserted article: {title}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Stopped by user.")

if __name__ == "__main__":
    schedule_news_generation()
