# -*- coding: cp1251 -*-

# Імпортуємо необхідні модулі і бібліотеки
from ast import Return
from urllib import response, request as urllib_request
from googleapiclient.discovery import build
import pprint as pprint
from flask import Flask, jsonify, render_template, request as flask_request
from flask_sqlalchemy import SQLAlchemy

# Ініціалізуємо Flask додаток
app = Flask(__name__)

# Конфігуруємо базу даних SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///like_dislike.db'
db = SQLAlchemy(app)

# Створюємо моделі для таблиць бази даних
class Liked_video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    User_Id = db.Column(db.String(30), nullable=False)
    Video_id = db.Column(db.String(50), nullable=False)

class Searched_content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Search_request = db.Column(db.String(100), nullable=False)
    Search_data = db.Column(db.JSON, nullable=False)


# Описуємо маршрути і функції для них
@app.route('/data_search', methods=['POST'])
def get_data_from_youtube():
    
    #Отримуємо дані з запиту
    Search_request = flask_request.form.get('Search_request')   
    
    #Отримуємо дані з бази даних
    with app.app_context():
        videos = Searched_content.query.all()
        
    #Шукаємо чи є вже такий пошуковий запис в базі даних   
    for video in videos:
        if(video.Search_request == Search_request):
            return video.Search_data     

    api_key = "AIzaSyDLM40MIs5ueWjQ6sNoJq1VtuNl9DjuHEg"

    # Ініціалізуємо об'єкт YouTube API
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Виконуємо запит до YouTube API для пошуку відео
    urllib_request = youtube.search().list(
            part = 'snippet',
            q = Search_request,
            maxResults = 10,
            type ='video'
        )
    response = urllib_request.execute()

    # Зберігаємо результат пошуку у базі даних
    with app.app_context():
        first_item = Searched_content()
        first_item.Search_data = response
        first_item.Search_request = Search_request
        db.session.add(first_item)
        db.session.commit()

    return response


@app.route('/like_video', methods=['POST'])
def like_video():
    # Отримуємо дані від користувача через POST-запит
    User = flask_request.form.get('User')
    Video_id = flask_request.form.get('Video_id')

    # Зберігаємо дані про вподобане відео у базі даних
    with app.app_context():
        video = Liked_video()
        video.User_Id = User
        video.Video_id = Video_id
        db.session.add(video)
        db.session.commit()

    if Video_id:
        return f"Дані записані"
    else:
        return "Дані НЕ записані"


@app.route('/liked_videos_data')
def liked_videos():
    # Отримуємо дані про вподобані відео з бази даних
    with app.app_context():
        videos = Liked_video.query.all()
        video_list = [{'User_Id': video.User_Id, 'Video_id': video.Video_id} for video in videos]

    # Повертаємо JSON-відповідь з даними про вподобані відео
    return jsonify(video_list)


# Запускаємо додаток, якщо це основний файл
if __name__ == '__main__':
    app.run(debug=True)
