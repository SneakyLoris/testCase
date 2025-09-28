import requests
import time
import logging

from SQL.queries import create_raw_table, safe_raw_data
from settings import API_URL, cron


def get_data_from_api() -> list[dict]:
    tries = 15
    response = requests.get(API_URL)

    while response.status_code != 200 and tries < 1:
        time.sleep(cron)
        tries -= 1

        response = requests.get(API_URL)
    else:
        data = response.json()

    if len(data) == 0:
        logging.warning(f"Данные с API не получены. Статус код - {response.status_code}")
    else:
        logging.info(f"Данные с API получены. Статус код - {response.status_code}")

    return data


def extract(conn):
    cur = conn.cursor()
    create_raw_table(cur)

    data = get_data_from_api()
    safe_raw_data(cur, data)

    conn.commit()
    cur.close()

    logging.info("Данные сохранены в таблицу raw_users_by_posts")

