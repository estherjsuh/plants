[![CircleCI](https://circleci.com/github/estherjsuh/plants?style=svg)](https://app.circleci.com/github/estherjsuh/plants)


![alt text](https://github.com/estherjsuh/plants/blob/master/static/technologies.png)


# Plant App

## Created By Esther Suh

## Description
🌱🍃🌿🌱🌵Inspired by the joy of raising houseplants 🌱🍃🌿🌱🌵

Looking at photos of nature could lower stress and lighten moods.

## How It's Made
### Key Python Modules
 - Flask - web Framework
 - SQLAlchemy - ORM
 - Flask-WTF - forms
 - Jinja2 - templating engine
 - flask-login - logging users
 - flask-bcrypt - password hashing
 - nose2 - unit testing
 - boto3 - upload images to S3

This application is written using Python 3.7 The database used is PostgreSQL.

### Deployment
 - App deployed on Heroku
 - Uploaded images stored within Amazon S3

Deployed application can be found here: https://plants-app-api.herokuapp.com/


## Install & Run App:
1. clone this repo
```
git clone git@github.com:estherjsuh/plants.git
```

2. cd into plants
```
cd plants
```

3. create virual environment and install dependencies
```
virtualenv venv --python=python3.7
source venv/bin/activate
pip install -r requirements.txt
```

4. run python
```
python
import project
app =  project.create_app()
app.run()
```

## Running Tests
From the root directory, run:
```
nose2
```
