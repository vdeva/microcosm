import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the database URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Function to get all table names in the public schema
def get_table_names(cursor):
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """)
    return [row[0] for row in cursor.fetchall()]

# Function to truncate all tables
def truncate_all_tables(cursor, tables):
    for table in tables:
        cursor.execute(sql.SQL("TRUNCATE TABLE {} CASCADE").format(sql.Identifier(table)))

# Function to reset sequences
def reset_sequences(cursor, tables):
    for table in tables:
        cursor.execute(sql.SQL("""
            SELECT column_default
            FROM information_schema.columns
            WHERE table_name = %s AND column_default LIKE 'nextval%%'
        """), [table])
        result = cursor.fetchone()
        if result:
            sequence_name = result[0].split("'")[1]
            cursor.execute(sql.SQL("ALTER SEQUENCE {} RESTART WITH 1").format(sql.Identifier(sequence_name)))

# Connect to the PostgreSQL database
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

try:
    # Get all table names
    table_names = get_table_names(cursor)
    print(f"Tables to truncate: {table_names}")

    # Truncate all tables
    truncate_all_tables(cursor, table_names)

    # Reset sequences
    reset_sequences(cursor, table_names)

    # Commit the transaction
    conn.commit()
    print("All tables have been truncated and sequences reset successfully.")
except Exception as e:
    print(f"Error: {e}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()
