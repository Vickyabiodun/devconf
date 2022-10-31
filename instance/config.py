from flask import Flask

DEBUG=True
FLASK_ENVIRONMENT='development'
SECRET_KEY='M8PmhNk8wh+e*$!+)7LH$U'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root@localhost/dev'
SQLALCHEMY_TRACK_MODIFICATIONS=False