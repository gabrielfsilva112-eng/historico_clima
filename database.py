import os
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

url = urlparse(os.getenv("DATABASE_URL"))

DB_CONFIG = {
    "host":     url.hostname,
    "port":     url.port,
    "dbname":   url.path[1:],
    "user":     url.username,
    "password": url.password,
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def criar_tabela():
    sql = """
        CREATE TABLE IF NOT EXISTS historico_clima (
            id           SERIAL PRIMARY KEY,
            cidade       VARCHAR(100) NOT NULL,
            data         VARCHAR(20)  NOT NULL,
            umidade      FLOAT,
            vento        FLOAT,
            precipitacao FLOAT,
            temp_min     FLOAT,
            temp_max     FLOAT
        );
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()

def ja_existe_registro(cidade, data):
    sql = "SELECT 1 FROM historico_clima WHERE cidade = %s AND data = %s"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (cidade, data))
            return cur.fetchone() is not None

def insert_clima(cidade, data, umidade, vento, precipitacao, temp_min, temp_max):
    sql = """
        INSERT INTO historico_clima (cidade, data, umidade, vento, precipitacao, temp_min, temp_max)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (cidade, data, umidade, vento, precipitacao, temp_min, temp_max))
        conn.commit()