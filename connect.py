import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD

conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
cursor = conn.cursor()

