from SQL.queries import get_raw_data, create_vitrine_table, safe_vitrine_data
import logging


def transform(conn):
    cur = conn.cursor()

    data = get_raw_data(cur)

    create_vitrine_table(cur)
    safe_vitrine_data(cur, data)
    conn.commit()

    cur.close()
    logging.info("Данные загружены в витрину top_users_by_posts")
