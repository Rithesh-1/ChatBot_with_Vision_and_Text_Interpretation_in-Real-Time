import os
class config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Entering Key' #Key Specify
    SQLALCHEMY_DATABASE_URI = 'sqlit: URI (link)'
    SQLALCHEMY_TRACK_MODIFICATIONS =False
    JWT_SECRET_KEY ='JWT(key)'#KEy specify