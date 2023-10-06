# -*- coding: cp1251 -*-

# Іmport the necessary modules and libraries
from urllib import response, request as urllib_request
from googleapiclient.discovery import build
from flask import Flask, jsonify, render_template, request as flask_request
from flask_sqlalchemy import SQLAlchemy
from DB_models import LikedVideo, SearchedContent, db as models_db
from Api import return_api_key

# Іnitialize the Flask application
app = Flask(__name__)
# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///like_dislike.db'

models_db.init_app(app)

# Describe the routes and their functions
@app.route('/video/data', methods=['POST'])
def get_data_from_youtube():
    
    # Receive data from the request
    search_request = flask_request.form.get('Search_request') 
    
    # check whether such a search record already exists in the database
    with app.app_context():
        existing_record = SearchedContent.query.filter_by(Search_request=search_request).first()

    if existing_record:
        return existing_record.Search_data    

    # Initialize the YouTube API object
    youtube = build('youtube', 'v3', developerKey=return_api_key())

    # Make a request to the YouTube API to search for videos
    urllib_request = youtube.search().list(
            part = 'snippet',
            q = search_request,
            maxResults = 10,
            type ='video'
        )
    response = urllib_request.execute()

    # Save the search result in the database
    with app.app_context():
        first_item = SearchedContent()
        first_item.Search_data = response
        first_item.Search_request = search_request
        models_db.session.add(first_item)
        models_db.session.commit()

    return response


@app.route('/video/like', methods=['POST'])
def like_video():
    # Receive data from the user through a POST request
    user = flask_request.form.get('User')
    video_id = flask_request.form.get('Video_id')

    # Checking the presence of Video_id in the database
    with app.app_context():
        existing_video = LikedVideo.query.filter_by(User_Id=user, Video_id=video_id).first()

        if existing_video:
            return f"Відео {video_id} вже присутнє у вподобаних користувача {user}"
        
        # Store data about favorite videos in the database
        video = LikedVideo()
        video.User_Id = user
        video.Video_id = video_id
        models_db.session.add(video)
        models_db.session.commit()
        return f"Відео {video_id} додано до вподобаних користувача {user}"


@app.route('/video/like/remove', methods=['POST'])
def remove_liked_video():
    # Get data from the user via a POST request
    User = flask_request.form.get('User')
    Video_id = flask_request.form.get('Video_id')

    # Checking for a record in a table and deleting it if it exists
    with app.app_context():
        video = LikedVideo.query.filter_by(User_Id=User, Video_id=Video_id).first()
        if video:
            models_db.session.delete(video)
            models_db.session.commit()
            return f"Відео {Video_id} видалено з вподобаних користувача {User}"
        return f"Відео {Video_id} не знайдено у вподобаних користувача {User}"


@app.route('/video/like/data/all')
def liked_videos():
    # Receive data about favorite videos from the database
    with app.app_context():
        videos = LikedVideo.query.all()
        video_list = [{'User_Id': video.User_Id, 'Video_id': video.Video_id} for video in videos]

    # Return a JSON response with data about liked videos
    return jsonify(video_list)

@app.route('/video/like/data', methods=['POST'])
def liked_user_videos():
    # Get the User_Id of the current user
    User = flask_request.form.get('User')

    # Receive data about favorite videos for a specific user from the database
    with app.app_context():
        videos = LikedVideo.query.filter_by(User_Id=User).all()
        video_list = [{'User_Id': video.User_Id, 'Video_id': video.Video_id} for video in videos]

    # Return a JSON response with data about favorite videos for a specific user
    return jsonify(video_list)


# Launch the application if it is the main file
if __name__ == '__main__':
    app.run(debug=True)
