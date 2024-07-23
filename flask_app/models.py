from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../weather_scraper/weather_scraper/spiders/weather_data.db'  # 更新数据库路径
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class WeatherData(db.Model):
    __tablename__ = 'hourly_forecast'  # 使用实际的表名
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    temperature = db.Column(db.String, nullable=False)
    humidity = db.Column(db.String, nullable=False)


def init_db():
    db.create_all()


if __name__ == '__main__':
    init_db()
