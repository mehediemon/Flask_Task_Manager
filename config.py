import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://task_manager_user:12345678@127.0.0.1/task_manager_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False