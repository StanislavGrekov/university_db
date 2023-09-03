import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD

conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host='127.0.0.1', port="5433")

# conn = psycopg2.connect('postgresql://postgres:masterkey@127.0.0.1:5433/bank_db') # Можно так подключиться
cursor = conn.cursor()

