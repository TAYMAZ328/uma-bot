from dotenv import load_dotenv
import os

from database.database import DB


load_dotenv()
TOKEN = os.getenv("TOKEN")
API_HASH = os.getenv("API_HASH")
API_ID = os.getenv("API_ID")
OWNER = int(os.getenv("OWNER"))

HOST = os.getenv("HOST")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
DB_NAME = os.getenv("DB_NAME")


db = DB(host=HOST, username=USERNAME, password=PASSWORD, db_name=DB_NAME)
db.connect_db()