import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database and API settings
DATABASE_URL = os.getenv("DATABASE_URL")

# Data to be inserted
stocks_data = [
    ('AAPL', 'Apple Inc.', 'Technology company specializing in consumer electronics.'),
    ('GOOGL', 'Alphabet Inc.', 'Parent company of Google and several former Google subsidiaries.'),
    ('MSFT', 'Microsoft Corp.', 'Technology company known for its software products.'),
    ('TSLA', 'Tesla Inc.', 'Automaker and clean energy company.'),
    ('AMZN', 'Amazon.com Inc.', 'Multinational technology company focusing on e-commerce.')
]

# Connect to the database
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Create a SQL query for inserting data
insert_query = sql.SQL("""
    INSERT INTO {table} (symbol, name, info)
    VALUES %s
    ON CONFLICT (symbol) DO NOTHING
""").format(table=sql.Identifier('stocks'))

# Execute the query
execute_values(cur, insert_query, stocks_data)

# Commit the changes to the database
conn.commit()

# Close communication with the database
cur.close()
conn.close()

print("Stocks have been added successfully.")
