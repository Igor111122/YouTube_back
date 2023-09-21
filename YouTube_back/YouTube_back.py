# -*- coding: cp1251 -*-

# ��������� �������� ����� � ��������
from ast import Return
from urllib import response, request as urllib_request
from googleapiclient.discovery import build
import pprint as pprint
from flask import Flask, jsonify, render_template, request as flask_request
from flask_sqlalchemy import SQLAlchemy

# ���������� Flask �������
app = Flask(__name__)

# ����������� ���� ����� SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///like_dislike.db'
db = SQLAlchemy(app)

# ��������� ����� ��� ������� ���� �����
class Liked_video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    User_Id = db.Column(db.String(30), nullable=False)
    Video_id = db.Column(db.String(50), nullable=False)

class Searched_content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Search_request = db.Column(db.String(100), nullable=False)
    Search_data = db.Column(db.JSON, nullable=False)


# ������� �������� � ������� ��� ���
@app.route('/data_search', methods=['POST'])
def get_data_from_youtube():
    
    #�������� ��� � ������
    Search_request = flask_request.form.get('Search_request')   
    
    #�������� ��� � ���� �����
    with app.app_context():
        videos = Searched_content.query.all()
        
    #������ �� � ��� ����� ��������� ����� � ��� �����   
    for video in videos:
        if(video.Search_request == Search_request):
            return video.Search_data     

    api_key = "AIzaSyDLM40MIs5ueWjQ6sNoJq1VtuNl9DjuHEg"

    # ���������� ��'��� YouTube API
    youtube = build('youtube', 'v3', developerKey=api_key)

    # �������� ����� �� YouTube API ��� ������ ����
    urllib_request = youtube.search().list(
            part = 'snippet',
            q = Search_request,
            maxResults = 10,
            type ='video'
        )
    response = urllib_request.execute()

    # �������� ��������� ������ � ��� �����
    with app.app_context():
        first_item = Searched_content()
        first_item.Search_data = response
        first_item.Search_request = Search_request
        db.session.add(first_item)
        db.session.commit()

    return response


@app.route('/like_video', methods=['POST'])
def like_video():
    # �������� ��� �� ����������� ����� POST-�����
    User = flask_request.form.get('User')
    Video_id = flask_request.form.get('Video_id')

    # �������� ��� ��� ��������� ���� � ��� �����
    with app.app_context():
        video = Liked_video()
        video.User_Id = User
        video.Video_id = Video_id
        db.session.add(video)
        db.session.commit()

    if Video_id:
        return f"��� �������"
    else:
        return "��� �� �������"


@app.route('/liked_videos_data')
def liked_videos():
    # �������� ��� ��� �������� ���� � ���� �����
    with app.app_context():
        videos = Liked_video.query.all()
        video_list = [{'User_Id': video.User_Id, 'Video_id': video.Video_id} for video in videos]

    # ��������� JSON-������� � ������ ��� �������� ����
    return jsonify(video_list)


# ��������� �������, ���� �� �������� ����
if __name__ == '__main__':
    app.run(debug=True)
