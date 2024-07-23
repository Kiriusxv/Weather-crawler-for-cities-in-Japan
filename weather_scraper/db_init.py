import sqlite3

# 连接数据库（如果数据库不存在，则会创建一个新的数据库）
conn = sqlite3.connect('weather_scraper/spiders/weather_data.db')
cursor = conn.cursor()

# 启用外键支持
conn.execute('PRAGMA foreign_keys = ON')

# # 创建城市表，用于存储城市信息
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS city (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT UNIQUE
#     )
# ''')

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

# 提交更改并关闭连接
conn.commit()
conn.close()
