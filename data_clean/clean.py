import os
import re
import pandas as pd
import sqlite3
from scipy.stats import zscore
from sklearn.preprocessing import MinMaxScaler

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

# 关闭连接
conn.close()

# 将数据保存为CSV文件
daily_forecast_df.to_csv('daily_forecast.csv', index=False)
hourly_forecast_df.to_csv('hourly_forecast.csv', index=False)
today_weather_df.to_csv('today_weather.csv', index=False)

# 数据清理函数
def clean_temperature(temp_str):
    if isinstance(temp_str, str):
        temp_str = re.sub(r'[^\d.]+', '', temp_str)  # 移除非数字字符
    try:
        return float(temp_str)
    except ValueError:
        return None

# 对daily_forecast表进行数据清洗
daily_forecast_df = pd.read_csv('daily_forecast.csv')
daily_forecast_df.dropna(inplace=True)
daily_forecast_df.drop_duplicates(inplace=True)
daily_forecast_df['high_temp'] = daily_forecast_df['high_temp'].apply(clean_temperature).astype(float)
daily_forecast_df['low_temp'] = daily_forecast_df['low_temp'].apply(clean_temperature).astype(float)
threshold_high = daily_forecast_df['high_temp'].mean() + 3 * daily_forecast_df['high_temp'].std()
threshold_low = daily_forecast_df['low_temp'].mean() + 3 * daily_forecast_df['low_temp'].std()
daily_forecast_df.loc[daily_forecast_df['high_temp'] > threshold_high, 'high_temp'] = daily_forecast_df['high_temp'].mean()
daily_forecast_df.loc[daily_forecast_df['low_temp'] > threshold_low, 'low_temp'] = daily_forecast_df['low_temp'].mean()
daily_forecast_df.to_csv('cleaned_daily_forecast.csv', index=False)

# 对hourly_forecast表进行数据清洗
hourly_forecast_df = pd.read_csv('hourly_forecast.csv')
hourly_forecast_df.dropna(inplace=True)
hourly_forecast_df.drop_duplicates(inplace=True)
hourly_forecast_df['temperature'] = hourly_forecast_df['temperature'].apply(clean_temperature)

# 打印清理后无法转换的值
print(hourly_forecast_df[hourly_forecast_df['temperature'].isnull()])

# 转换为浮点数
hourly_forecast_df['temperature'] = hourly_forecast_df['temperature'].astype(float)

threshold_temp = hourly_forecast_df['temperature'].mean() + 3 * hourly_forecast_df['temperature'].std()
hourly_forecast_df.loc[hourly_forecast_df['temperature'] > threshold_temp, 'temperature'] = hourly_forecast_df['temperature'].mean()
hourly_forecast_df.to_csv('cleaned_hourly_forecast.csv', index=False)

# 对today_weather表进行数据清洗
today_weather_df = pd.read_csv('today_weather.csv')
today_weather_df.dropna(inplace=True)
today_weather_df.drop_duplicates(inplace=True)
today_weather_df['temperature'] = today_weather_df['temperature'].apply(clean_temperature).astype(float)
today_weather_df['realfeel'] = today_weather_df['realfeel'].apply(clean_temperature).astype(float)
today_weather_df['wind'] = today_weather_df['wind'].apply(clean_temperature).astype(float)
today_weather_df['gust'] = today_weather_df['gust'].apply(clean_temperature).astype(float)
threshold_temp = today_weather_df['temperature'].mean() + 3 * today_weather_df['temperature'].std()
today_weather_df.loc[today_weather_df['temperature'] > threshold_temp, 'temperature'] = today_weather_df['temperature'].mean()
today_weather_df.to_csv('cleaned_today_weather.csv', index=False)
