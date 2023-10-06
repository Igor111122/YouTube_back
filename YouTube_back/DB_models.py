from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Створюємо моделі для таблиць бази даних
class LikedVideo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    User_Id = db.Column(db.String(30), nullable=False)
    Video_id = db.Column(db.String(50), nullable=False)

class SearchedContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Search_request = db.Column(db.String(100), nullable=False)
    Search_data = db.Column(db.JSON, nullable=False)
