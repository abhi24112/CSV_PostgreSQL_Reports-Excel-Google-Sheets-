import psycopg2
import os
from dotenv import load_dotenv
import logging

# By default looks for the .env fils
load_dotenv()

logger = logging.getLogger(__name__)

class DatabaseManager:

    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.database = os.getenv("DB_DATABASE")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.port = os.getenv("DB_PORT")

        self.conn = None
        self.cur = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host = self.host,
                database = self.database,
                user = self.user,
                password = self.password,
                port = self.port
            )

            self.cur = self.conn.cursor()

            logger.info("Database connected successfully")
        except Exception as e:
            raise Exception(f"DB Connection failed: {e}")
        
    def execute_query(self, query, params=None):
        if self.cur is None:
            raise Exception("cur is None, need to call connect() for initialize the cur.")
        self.cur.execute(query, params)

    def fetch_all(self):
        if self.cur is None:
            raise Exception("cur is None, need to call connect() for initialize the cur.")
        return self.cur.fetchall()
        
    def commit(self):
        if self.conn is None:
            raise Exception("cur is None, need to call connect() for initialize the cur.")
        self.conn.commit()

    def rollback(self):
        if self.conn is None:
            raise Exception("cur is None, need to call connect() for initialize the cur.")
        self.conn.rollback()

    def close(self):
        if self.cur:
            self.cur.close()

        if self.conn:
            self.conn.close()

        logger.info("Database connection closed")

    
    
