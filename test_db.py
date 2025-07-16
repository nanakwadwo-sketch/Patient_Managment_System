from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

dotenv_path = "E:\\health_app\\.env"
if not os.path.exists(dotenv_path):
    print(f"Error: .env file not found at {dotenv_path}")
else:
    print(f".env file found at {dotenv_path}")
load_dotenv(dotenv_path=dotenv_path)
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"DATABASE_URL: {DATABASE_URL}")
if DATABASE_URL is None:
    print("Error: DATABASE_URL is not set in .env file")
else:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        print("Connection successful!")
        from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Ensure the .env file is loaded correctly
dotenv_path = "E:\\health_app\\.env"
if not os.path.exists(dotenv_path):
    print(f"Error: .env file not found at {dotenv_path}")
else:
    print(f".env file found at {dotenv_path}")
load_dotenv(dotenv_path=dotenv_path)
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"DATABASE_URL: {DATABASE_URL}")
if DATABASE_URL is None:
    print("Error: DATABASE_URL is not set in .env file")
else:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        print("Connection successful!")