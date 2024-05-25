import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os
import random
import math

# Load environment variables from .env file
load_dotenv()

# Retrieve the database URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to the PostgreSQL database
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

def get_all_human_ids(cursor):
    cursor.execute("SELECT id FROM human;")
    return [row[0] for row in cursor.fetchall()]

def exponential_decay(avg_followers):
    """ Generate a random number with exponential decay probability distribution based on average followers. """
    scale = avg_followers / math.log(2)  # This adjustment aims to make the mean of the distribution close to avg_followers
    return int(random.expovariate(1 / scale))

def create_follow_relations(cursor, human_ids, avg_followers):
    max_follows = len(human_ids) - 1

    for follower_id in human_ids:
        # Determine a random number of follows with exponential decay
        number_of_follows = exponential_decay(avg_followers)
        number_of_follows = min(number_of_follows, max_follows)  # Ensure it does not exceed the max possible

        # Select random humans to follow
        following_ids = random.sample([id for id in human_ids if id != follower_id], number_of_follows)

        # Insert follow relationships into the database
        for following_id in following_ids:
            try:
                cursor.execute(
                    sql.SQL("INSERT INTO user_followers (follower_id, following_id) VALUES (%s, %s)"),
                    (follower_id, following_id)
                )
            except psycopg2.IntegrityError:
                # Handle cases where the relationship might already exist
                conn.rollback()

def get_top_followers(cursor):
    cursor.execute("""
    SELECT following_id, COUNT(follower_id) AS num_followers
    FROM user_followers
    GROUP BY following_id
    ORDER BY num_followers DESC
    LIMIT 10;
    """)
    return cursor.fetchall()

try:
    # Fetch all human IDs from the database
    human_ids = get_all_human_ids(cursor)

    avg_followers = 50  # Specify the average number of followers here

    # Create random follow relationships among humans
    create_follow_relations(cursor, human_ids, avg_followers)

    # Commit the transaction
    conn.commit()
    
    # Get and print the top 10 humans with the most followers
    top_followers = get_top_followers(cursor)
    print("Top 10 humans with the most followers:")
    for following_id, num_followers in top_followers:
        print(f"Human ID: {following_id}, Followers: {num_followers}")

    print("Follow relationships created successfully.")
except Exception as e:
    print(f"Error: {e}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()
