import psycopg2
from psycopg2 import sql
from faker import Faker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the database URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Initialize Faker
fake = Faker()

# Function to create a new human record
def create_human():
    name = fake.name()
    address = fake.address()
    username = fake.user_name()
    return (name, address, username)

# Function to check if a username exists
def username_exists(cursor, username):
    cursor.execute("SELECT 1 FROM Human WHERE username = %s", (username,))
    return cursor.fetchone() is not None

# Function to insert a human record into the database
def insert_human(cursor, human):
    insert_query = sql.SQL(
        "INSERT INTO Human (name, address, username) VALUES (%s, %s, %s) RETURNING id"
    )
    cursor.execute(insert_query, human)
    return cursor.fetchone()[0]

# Connect to the PostgreSQL database
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Generate and insert fake human records
try:
    for _ in range(10000):  # Generate fake humans
        while True:
            human = create_human()
            if not username_exists(cursor, human[2]):
                human_id = insert_human(cursor, human)
                print(f"Inserted human with ID: {human_id}")
                break
    
    # Commit the transaction
    conn.commit()
except Exception as e:
    print(f"Error: {e}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()
