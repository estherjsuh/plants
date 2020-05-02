![alt text](https://github.com/estherjsuh/plants/blob/master/static/technologies.png)


# Plant App

## Created By: Esther Suh

## Description
Inspired by the joy of raising houseplants

## Install & Run App:
1. fork this repo
```
git fork git@github.com:estherjsuh/plants.git
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

##Running Tests
From the root directory, run:
```
nose2
```


## How It's Made
### Key Python Modules
 - Flask - web Framework
 - Jinja2 - templating engine
 - SQLAlchemy - ORM
 - Flask-WTF - form
 - flask-login - logging users
 - nose2 - unit testing

This application is written using Python 3.7.1. The database used is PostgreSQL.
