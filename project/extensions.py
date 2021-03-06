from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import boto3
import os

S3_KEY= os.environ.get("AWS_ACCESS_KEY_ID")
S3_SECRET = os.environ.get("AWS_SECRET_ACCESS_KEY")
S3_BUCKET = os.environ.get("AWS_BUCKET_NAME")
BUCKET_PREFIX = os.environ.get('BUCKET_PREFIX')

login_manager = LoginManager()
db = SQLAlchemy()
bcrypt = Bcrypt()


session = boto3.Session(aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET)
s3 = session.resource('s3')
