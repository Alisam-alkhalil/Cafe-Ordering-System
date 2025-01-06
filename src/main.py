import psycopg
import os
from dotenv import load_dotenv
from database import create_database

load_dotenv()

dbname = os.getenv('POSTGRES_DB')
host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_PORT')
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')

conn = psycopg.connect(
    dbname=dbname,
    host=host,
    port=port,
    user=user,
    password=password
    
)

def main():
    create_database(conn)


if __name__ == '__main__':
    main()