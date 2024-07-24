import sqlite3
import csv


def get_db_connection():
    db_path = 'weather_data.db'
    return sqlite3.connect(db_path)


def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 创建city表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS city (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            url TEXT
        )
    ''')

    # 创建today_weather表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS today_weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            temperature TEXT,
            realfeel TEXT,
            wind TEXT,
            gust TEXT,
            air_quality TEXT,
            FOREIGN KEY (city) REFERENCES city(name)
        )
    ''')

    # 创建hourly_forecast表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hourly_forecast (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            time TEXT,
            temperature TEXT,
            humidity TEXT,
            FOREIGN KEY (city) REFERENCES city(name)
        )
    ''')

    # 创建daily_forecast表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_forecast (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            date TEXT,
            high_temp TEXT,
            low_temp TEXT,
            detail_weather TEXT,
            humidity TEXT,
            FOREIGN KEY (city) REFERENCES city(name)
        )
    ''')

    conn.commit()
    conn.close()


def import_cities_from_csv():
    conn = get_db_connection()
    cursor = conn.cursor()

    with open('weather_scraper/weather_scraper/city.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute('''
                INSERT INTO city (name, url) VALUES (?, ?)
            ''', (row['city_name'], row['city_url']))

    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_tables()
    import_cities_from_csv()
    print("Database initialized and cities imported.")
