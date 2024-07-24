import os
import re
import pandas as pd
import sqlite3

# 获取当前脚本的目录
base_dir = os.path.dirname(os.path.abspath(__file__))

# 构建数据库文件的绝对路径
db_path = os.path.join(base_dir, '..', 'weather_scraper', 'weather_scraper', 'spiders', 'weather_data.db')

# 打印数据库路径
print(f"Database path: {db_path}")

# 检查文件是否存在
if not os.path.exists(db_path):
    raise FileNotFoundError(f"The database file does not exist at the path: {db_path}")

# 连接到 SQLite 数据库
conn = sqlite3.connect(db_path)

# 查询数据
daily_forecast_df = pd.read_sql("SELECT * FROM daily_forecast", conn)
hourly_forecast_df = pd.read_sql("SELECT * FROM hourly_forecast", conn)
today_weather_df = pd.read_sql("SELECT * FROM today_weather", conn)

# 获取所有城市名称
cities = pd.read_sql("SELECT DISTINCT name FROM city", conn)['name'].tolist()

# 关闭连接
conn.close()


# 数据清理和转换函数
def clean_and_convert_temperature(temp_str):
    if isinstance(temp_str, str):
        temp_str = re.sub(r'[^\d.]+', '', temp_str)  # 移除非数字字符
    try:
        temp_fahrenheit = float(temp_str)
        temp_celsius = (temp_fahrenheit - 32) * 5.0 / 9.0  # 转换为摄氏度
        return round(temp_celsius, 2)  # 保留两位小数
    except ValueError:
        return None


def clean_and_convert_humidity(humidity_str):
    if isinstance(humidity_str, str):
        humidity_str = re.sub(r'[^\d.]+', '', humidity_str)  # 移除非数字字符
    try:
        return round(float(humidity_str), 2)  # 保留两位小数
    except ValueError:
        return None


# 去除以 "N/A" 结尾的字符串中的 "N/A"
def remove_na_suffix(detail_str):
    if isinstance(detail_str, str) and detail_str.endswith("，N/A"):
        return detail_str[:-4]
    return detail_str


# 创建文件夹并保存数据
for city in cities:
    city_folder = os.path.join(base_dir, city)
    os.makedirs(city_folder, exist_ok=True)

    # 过滤出该城市的数据
    city_daily_forecast = daily_forecast_df[daily_forecast_df['city'] == city].copy()
    city_hourly_forecast = hourly_forecast_df[hourly_forecast_df['city'] == city].copy()
    city_today_weather = today_weather_df[today_weather_df['city'] == city].copy()

    # 清理和转换数据
    if 'high_temp' in city_daily_forecast.columns:
        city_daily_forecast.loc[:, 'high_temp'] = city_daily_forecast['high_temp'].apply(clean_and_convert_temperature)
    if 'low_temp' in city_daily_forecast.columns:
        city_daily_forecast.loc[:, 'low_temp'] = city_daily_forecast['low_temp'].apply(clean_and_convert_temperature)
    if 'humidity' in city_daily_forecast.columns:
        city_daily_forecast.loc[:, 'humidity'] = city_daily_forecast['humidity'].apply(clean_and_convert_humidity)
    if 'detail_weather' in city_daily_forecast.columns:
        city_daily_forecast.loc[:, 'detail_weather'] = city_daily_forecast['detail_weather'].apply(remove_na_suffix)

    if 'temperature' in city_hourly_forecast.columns:
        city_hourly_forecast.loc[:, 'temperature'] = city_hourly_forecast['temperature'].apply(
            clean_and_convert_temperature)
    if 'humidity' in city_hourly_forecast.columns:
        city_hourly_forecast.loc[:, 'humidity'] = city_hourly_forecast['humidity'].apply(clean_and_convert_humidity)

    if 'temperature' in city_today_weather.columns:
        city_today_weather.loc[:, 'temperature'] = city_today_weather['temperature'].apply(
            clean_and_convert_temperature)
    if 'realfeel' in city_today_weather.columns:
        city_today_weather.loc[:, 'realfeel'] = city_today_weather['realfeel'].apply(clean_and_convert_temperature)
    if 'wind' in city_today_weather.columns:
        city_today_weather.loc[:, 'wind'] = city_today_weather['wind'].apply(clean_and_convert_temperature)
    if 'gust' in city_today_weather.columns:
        city_today_weather.loc[:, 'gust'] = city_today_weather['gust'].apply(clean_and_convert_temperature)
    if 'humidity' in city_today_weather.columns:
        city_today_weather.loc[:, 'humidity'] = city_today_weather['humidity'].apply(clean_and_convert_humidity)

    # 保存清理和转换后的数据到对应的城市文件夹
    daily_forecast_path = os.path.join(city_folder, 'daily_forecast.csv')
    hourly_forecast_path = os.path.join(city_folder, 'hourly_forecast.csv')
    today_weather_path = os.path.join(city_folder, 'today_weather.csv')

    city_daily_forecast.to_csv(daily_forecast_path, index=False)
    city_hourly_forecast.to_csv(hourly_forecast_path, index=False)
    city_today_weather.to_csv(today_weather_path, index=False)

    print(f"Data for city {city} has been saved and cleaned.")

print("All data has been saved and cleaned.")
