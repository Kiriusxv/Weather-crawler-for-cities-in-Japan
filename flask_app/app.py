from flask import Flask, render_template, request, redirect, url_for, flash
import matplotlib.pyplot as plt
import pandas as pd
import os
import concurrent.futures

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于闪存消息

def generate_charts(city, high_temps, low_temps, daily_humidity, hourly_temps, hourly_humidity):
    # 确保城市的 static 目录存在
    static_dir = os.path.join(app.root_path, 'static', city)
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    # 创建 daily 高低温度图表
    plt.figure(figsize=(10, 6))
    plt.plot(high_temps, label='High Temperature', color='red')
    plt.plot(low_temps, label='Low Temperature', color='blue')
    plt.title(f'{city} Daily High and Low Temperatures')
    plt.xlabel('Day')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.savefig(os.path.join(static_dir, 'daily_temperature_chart.png'))
    plt.close()

    # 创建 daily 湿度图表
    plt.figure(figsize=(10, 6))
    plt.plot(daily_humidity, label='Humidity', color='green')
    plt.title(f'{city} Daily Humidity')
    plt.xlabel('Day')
    plt.ylabel('Humidity (%)')
    plt.legend()
    plt.savefig(os.path.join(static_dir, 'daily_humidity_chart.png'))
    plt.close()

    # 创建 hourly 温度图表
    plt.figure(figsize=(10, 6))
    plt.plot(hourly_temps, label='Temperature', color='orange')
    plt.title(f'{city} Hourly Temperatures')
    plt.xlabel('Hour')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.savefig(os.path.join(static_dir, 'hourly_temperature_chart.png'))
    plt.close()

    # 创建 hourly 湿度图表
    plt.figure(figsize=(10, 6))
    plt.plot(hourly_humidity, label='Humidity', color='purple')
    plt.title(f'{city} Hourly Humidity')
    plt.xlabel('Hour')
    plt.ylabel('Humidity (%)')
    plt.legend()
    plt.savefig(os.path.join(static_dir, 'hourly_humidity_chart.png'))
    plt.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    # 读取城市列表
    cities_dir = os.path.join(app.root_path, '../data_clean')
    cities = [name for name in os.listdir(cities_dir) if os.path.isdir(os.path.join(cities_dir, name))]

    if request.method == 'POST':
        city = request.form.get('city')
        return redirect(url_for('city_weather', city=city))
    return render_template('index.html', cities=cities)

@app.route('/weather/<city>')
def city_weather(city):
    # 文件路径
    daily_csv_file_path = os.path.join(app.root_path, f'../data_clean/{city}/daily_forecast.csv')
    hourly_csv_file_path = os.path.join(app.root_path, f'../data_clean/{city}/hourly_forecast.csv')
    today_csv_file_path = os.path.join(app.root_path, f'../data_clean/{city}/today_weather.csv')

    # 检查文件是否存在
    if not os.path.exists(daily_csv_file_path) or not os.path.exists(hourly_csv_file_path) or not os.path.exists(today_csv_file_path):
        flash(f'Weather data for {city} is not available.')
        return redirect(url_for('index'))

    # 读取 daily_forecast.csv 文件
    daily_data = pd.read_csv(daily_csv_file_path)
    daily_data['high_temp'] = daily_data['high_temp'].astype(str)
    daily_data['low_temp'] = daily_data['low_temp'].astype(str)
    daily_data['humidity'] = daily_data['humidity'].astype(str)
    high_temps = daily_data['high_temp'].str.replace('°', '').astype(float)
    low_temps = daily_data['low_temp'].str.replace('°', '').astype(float)
    daily_humidity = daily_data['humidity'].str.replace('%', '').astype(float)

    # 读取 hourly_forecast.csv 文件
    hourly_data = pd.read_csv(hourly_csv_file_path)
    hourly_data['temperature'] = hourly_data['temperature'].astype(str)
    hourly_data['humidity'] = hourly_data['humidity'].astype(str)
    hourly_temps = hourly_data['temperature'].str.replace('°', '').astype(float)
    hourly_humidity = hourly_data['humidity'].str.replace('%', '').astype(float)

    # 读取 today_weather.csv 文件
    today_data = pd.read_csv(today_csv_file_path)
    if not today_data.empty:
        today_weather = today_data.iloc[0].to_dict()
    else:
        today_weather = None

    # 使用线程池并行生成图表
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(generate_charts, city, high_temps, low_temps, daily_humidity, hourly_temps, hourly_humidity)
        future.result()

    return render_template('city_weather.html', city=city, today_weather=today_weather, daily_data=daily_data)

if __name__ == '__main__':
    app.run(debug=True)
