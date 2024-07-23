from flask import Flask, render_template
import matplotlib.pyplot as plt
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
    # 读取 cleaned_daily_forecast.csv 文件
    daily_csv_file_path = os.path.join(app.root_path, '../data_clean/cleaned_daily_forecast.csv')
    daily_data = pd.read_csv(daily_csv_file_path)
    daily_data['high_temp'] = daily_data['high_temp'].astype(str)
    daily_data['low_temp'] = daily_data['low_temp'].astype(str)
    daily_data['humidity'] = daily_data['humidity'].astype(str)
    high_temps = daily_data['high_temp'].str.replace('°', '').astype(float)
    low_temps = daily_data['low_temp'].str.replace('°', '').astype(float)
    daily_humidity = daily_data['humidity'].str.replace('%', '').astype(float)

    # 读取 cleaned_hourly_forecast.csv 文件
    hourly_csv_file_path = os.path.join(app.root_path, '../data_clean/cleaned_hourly_forecast.csv')
    hourly_data = pd.read_csv(hourly_csv_file_path)
    hourly_data['temperature'] = hourly_data['temperature'].astype(str)
    hourly_data['humidity'] = hourly_data['humidity'].astype(str)
    hourly_temps = hourly_data['temperature'].str.replace('°', '').astype(float)
    hourly_humidity = hourly_data['humidity'].str.replace('%', '').astype(float)

    # 读取 cleaned_today_weather.csv 文件
    today_csv_file_path = os.path.join(app.root_path, '../data_clean/cleaned_today_weather.csv')
    today_data = pd.read_csv(today_csv_file_path)
    today_weather = today_data.iloc[0]

    # 确保 static 目录存在
    static_dir = os.path.join(app.root_path, 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    # 创建 daily 高低温度图表
    plt.figure(figsize=(10, 6))
    plt.plot(high_temps, label='High Temperature', color='red')
    plt.plot(low_temps, label='Low Temperature', color='blue')
    plt.title('Daily High and Low Temperatures')
    plt.xlabel('Day')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.savefig(os.path.join(static_dir, 'daily_temperature_chart.png'))
    plt.close()

    # 创建 daily 湿度图表
    plt.figure(figsize=(10, 6))
    plt.plot(daily_humidity, label='Humidity', color='green')
    plt.title('Daily Humidity')
    plt.xlabel('Day')
    plt.ylabel('Humidity (%)')
    plt.legend()
    plt.savefig(os.path.join(static_dir, 'daily_humidity_chart.png'))
    plt.close()

    # 创建 hourly 温度图表
    plt.figure(figsize=(10, 6))
    plt.plot(hourly_temps, label='Temperature', color='orange')
    plt.title('Hourly Temperatures')
    plt.xlabel('Hour')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.savefig(os.path.join(static_dir, 'hourly_temperature_chart.png'))
    plt.close()

    # 创建 hourly 湿度图表
    plt.figure(figsize=(10, 6))
    plt.plot(hourly_humidity, label='Humidity', color='purple')
    plt.title('Hourly Humidity')
    plt.xlabel('Hour')
    plt.ylabel('Humidity (%)')
    plt.legend()
    plt.savefig(os.path.join(static_dir, 'hourly_humidity_chart.png'))
    plt.close()

    return render_template('index.html', today_weather=today_weather)

if __name__ == '__main__':
    app.run(debug=True)
