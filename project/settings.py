import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SECRET_KEY = os.environ.get('SECRET')
SQLALCHEMY_TRACK_MODIFICATIONS = False
TOP_LEVEL_DIR = os.path.abspath(os.curdir)
UPLOAD_FOLDER = TOP_LEVEL_DIR + 'project/static/img/'
IMAGE_URL = '/static/img'
WTF_CSRF_ENABLED = True
#MAX_CONTENT_LENGTH = 16 * 1024 * 1024
