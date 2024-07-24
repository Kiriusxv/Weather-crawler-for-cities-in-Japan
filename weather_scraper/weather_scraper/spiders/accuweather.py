import os
import re
import sqlite3
import scrapy
import csv
from html import unescape
from scrapy.http import Request

class AccuweatherSpider(scrapy.Spider):
    name = 'accuweather'
    allowed_domains = ['accuweather.com']

    def start_requests(self):
        # 动态获取项目根目录
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        csv_path = os.path.join(project_root, 'city.csv')

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield scrapy.Request(url=row['city_url'], callback=self.parse, meta={'city': row['city_name']})

    def parse(self, response):
        city = response.meta['city']

        # 提取温度信息
        temperature = response.css('div.temp::text').re_first(r'\d+')
        temperature = temperature.strip() if temperature else 'N/A'

        # 提取RealFeel温度
        realfeel = response.css('div.real-feel::text').re_first(r'\d+')
        realfeel = realfeel.strip() if realfeel else 'N/A'

        # 提取风速
        wind_value = response.css('div.spaced-content.detail span.label:contains("風") + span.value::text').get(
            default='N/A').strip()

        # 提取大风信息
        gust_value = response.css('div.spaced-content.detail span.label:contains("風速") + span.value::text').get(
            default='N/A').strip()

        # 提取空气质量信息
        air_quality_value = response.css(
            'div.spaced-content.detail span.label:contains("空氣品質") + span.value::text').get(default='N/A').strip()

        # 打印提取到的信息到控制台
        self.log(f"Temperature: {temperature}")
        self.log(f"RealFeel Temperature: {realfeel}")
        self.log(f"Wind: {wind_value}")
        self.log(f"Gust: {gust_value}")
        self.log(f"Air Quality: {air_quality_value}")

        # 保存今日天气数据到数据库
        self.save_today_weather(city, temperature, realfeel, wind_value, gust_value, air_quality_value)

        # 提取每日天气预报的信息
        daily_forecasts = response.css('a.daily-list-item')
        for forecast in daily_forecasts:
            date = ''.join(forecast.css('div.date p::text').getall()).strip()
            high_temp = forecast.css('div.temp span.temp-hi::text').re_first(r'\d+')
            high_temp = high_temp.strip() if high_temp else 'N/A'
            low_temp = forecast.css('div.temp span.temp-lo::text').re_first(r'\d+')
            low_temp = low_temp.strip() if low_temp else 'N/A'
            day_phrase = forecast.css('div.phrase p.no-wrap::text').get(default='N/A').strip()
            night_phrase = forecast.css('div.phrase span.night p.no-wrap::text').get(default='N/A').strip()
            detail_weather = f"{day_phrase}，{night_phrase}"
            humidity = forecast.css('div.precip').xpath('text()').re_first(r'\d+%')
            humidity = humidity.strip() if humidity else 'N/A'

            # 打印提取到的每日天气信息到控制台
            self.log(f"Date: {date}")
            self.log(f"High Temp: {high_temp}")
            self.log(f"Low Temp: {low_temp}")
            self.log(f"Detail Weather: {detail_weather}")
            self.log(f"Humidity: {humidity}")

            # 保存每日预报数据到数据库
            self.save_daily_forecast(city, date, high_temp, low_temp, detail_weather, humidity)

        # 提取小时预报项
        hourly_forecast_items = response.css('.hourly-list__list__item')
        for item in hourly_forecast_items:
            # 提取时间
            time = unescape(item.css('.hourly-list__list__item-time::text').get(default='N/A').strip())

            # 提取温度
            temp = unescape(item.css('.hourly-list__list__item-temp::text').get(default='N/A').strip())

            # 提取湿度
            humidity = item.css('.hourly-list__list__item-precip span::text').get(default='N/A').strip()

            # 打印小时预报信息到日志
            self.log(f"Hourly Forecast - Time: {time}, Temperature: {temp}, Humidity: {humidity}")

            # 保存小时预报信息到数据库
            self.save_hourly_forecast(city, time, temp, humidity)

    def get_db_connection(self):
        # 获取当前脚本所在的目录
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, 'weather_data.db')
        return sqlite3.connect(db_path)


    def save_city(self, city):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS city (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
        ''')
        cursor.execute('''
            INSERT OR IGNORE INTO city (name) VALUES (?)
        ''', (city,))
        conn.commit()
        conn.close()

    def save_today_weather(self, city, temperature, realfeel, wind, gust, air_quality):
        conn = self.get_db_connection()
        cursor = conn.cursor()
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
        cursor.execute('''
            INSERT INTO today_weather (city, temperature, realfeel, wind, gust, air_quality)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (city, temperature, realfeel, wind, gust, air_quality))
        conn.commit()
        conn.close()

    def save_hourly_forecast(self, city, time, temp, humidity):
        conn = self.get_db_connection()
        cursor = conn.cursor()
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
        cursor.execute('''
            INSERT INTO hourly_forecast (city, time, temperature, humidity)
            VALUES (?, ?, ?, ?)
        ''', (city, time, temp, humidity))
        conn.commit()
        conn.close()

    def save_daily_forecast(self, city, date, high_temp, low_temp, detail_weather, humidity):
        conn = self.get_db_connection()
        cursor = conn.cursor()
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
        cursor.execute('''
            INSERT INTO daily_forecast (city, date, high_temp, low_temp, detail_weather, humidity)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (city, date, high_temp, low_temp, detail_weather, humidity))
        conn.commit()
        conn.close()