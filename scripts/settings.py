import logging

API_URL = "https://jsonplaceholder.typicode.com/posts"

DSN = "vk_project"
USER_NAME = "postgres"
DB_PASSWORD = "postgres"
CONNECTION_INFO = {
    "dbname": DSN,
    "user": USER_NAME,
    "password": DB_PASSWORD,
    "host": "dbps",
}

cron = 1  # сек
logging.basicConfig(level=logging.INFO)
