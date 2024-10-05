from dotenv import load_dotenv
import os

load_dotenv()


class Setting:
    url_db = os.getenv("DATABASE_URL")
    token = os.getenv("TOKEN")
    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM")
    expire = os.getenv("TTL")


settings = Setting()



