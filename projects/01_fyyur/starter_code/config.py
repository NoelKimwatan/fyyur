import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database

DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_NAME = os.getenv('DB_NAME', 'your_db')

SQLALCHEMY_DATABASE_URI = 'postgresql://{}@{}/{}'.format(DB_USER, DB_HOST, DB_NAME)

# # TODO IMPLEMENT DATABASE URL
# SQLALCHEMY_DATABASE_URI = 'postgresql://noelkimwatan@localhost:5432/fyyur'
SQLALCHEMY_TRACK_MODIFICATIONS = False
