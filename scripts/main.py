import logging

import psycopg2
import psycopg2.extras
from flask import Flask, jsonify

from extract import extract
from SQL.queries import get_vitrine_data
from settings import CONNECTION_INFO
from transform import transform

app = Flask(__name__)


@app.route('/')
def index():
    conn = psycopg2.connect(**CONNECTION_INFO)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    data = get_vitrine_data(cur)
    data = [dict(item) for item in data]

    cur.close()
    conn.close()

    return jsonify(data)


def main():
    # Подключение к бд
    conn = psycopg2.connect(**CONNECTION_INFO)

    # Выполнение первого скрипта
    extract(conn)

    # Выполнение второго скрипта
    transform(conn)

    conn.close()
    logging.info("Конец выполнения скриптов")


if __name__ == "__main__":
    main()

    app.run(debug=True, host="0.0.0.0", port=4000)
