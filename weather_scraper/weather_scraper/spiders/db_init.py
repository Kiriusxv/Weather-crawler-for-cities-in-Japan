import os
import sqlite3

# 获取当前脚本所在的目录
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'weather_data.db')

# 确保目录存在
os.makedirs(os.path.dirname(db_path), exist_ok=True)

try:
    # 连接到数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 创建city表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS city (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')

    # 创建今日天气表
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

    # 创建小时预报表
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

    # 创建每日预报表
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
    print("数据库初始化成功")

except sqlite3.OperationalError as e:
    print(f"SQLite 操作错误: {e}")
