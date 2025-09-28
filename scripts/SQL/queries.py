# Запросы для raw_table

## Запрос на создание таблицы
def create_raw_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS raw_users_by_posts (
        id SERIAL PRIMARY KEY,
        user_id INT,
        title TEXT,
        body TEXT
    )
    """)


## Запрос на сохранение\дополнения RAW таблицы
def safe_raw_data(cursor, data):
    prep_data = [(item["id"], item["userId"], item["title"], item["body"]) for item in data]
    cursor.executemany("""
            INSERT INTO raw_users_by_posts (id, user_id, title, body) 
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id)
            DO NOTHING
        """, prep_data)


## Запрос на получение данных из RAW таблицы в формате, который необходимо сохранить в витрину
def get_raw_data(cursor):
    cursor.execute("""
        SELECT user_id, COUNT(id) AS posts_cnt, CURRENT_TIMESTAMP AS calculated_at FROM raw_users_by_posts
        GROUP BY user_id
        ORDER BY posts_cnt
    """)

    return cursor.fetchall()


# Запросы к витрине

## Создание витрины
def create_vitrine_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS top_users_by_posts (
            user_id SERIAL PRIMARY KEY,
            posts_cnt INT,
            calculated_at TIMESTAMP
        )
        """)


## Добавление\обновление данных для витрины
def safe_vitrine_data(cursor, data):
    cursor.executemany("""
            INSERT INTO top_users_by_posts (user_id, posts_cnt, calculated_at) 
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id)
            DO UPDATE SET
            posts_cnt = EXCLUDED.posts_cnt,
            calculated_at = EXCLUDED.calculated_at
        """, data)


def get_vitrine_data(cursor):
    cursor.execute("""
            SELECT * FROM top_users_by_posts
            ORDER BY posts_cnt 
        """)
    return cursor.fetchall()