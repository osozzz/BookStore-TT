import time
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

load_dotenv()

DB_URI = os.getenv("DATABASE_URI")

if not DB_URI:
    print("❌ DATABASE_URI not found in .env")
    exit(1)

for attempt in range(30):  # 30 intentos (1 min)
    try:
        engine = create_engine(DB_URI)
        connection = engine.connect()
        connection.close()
        print("✅ DB is ready!")
        break
    except OperationalError:
        print(f"⏳ Waiting for DB... attempt {attempt+1}/30")
        time.sleep(5)
else:
    print("❌ DB is still not ready after retries")
    exit(1)
