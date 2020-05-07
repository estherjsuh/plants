import os
import unittest

#from project import app, db
from project import create_app
from project.models import Plants, User
from project.extensions import db
app = create_app()
app.app_context().push()

TEST_DB ='users.db'
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class UsersTest(unittest.TestCase):

    def setUp(self):
        with app.app_context():
            app.config['TESTING'] = True
            app.config['WTF_CSRF_ENABLED'] = False
            app.config['DEBUG'] = False
            app.config['SECRET_KEY'] = 'testing'
            #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.config['BASEDIR'], TEST_DB)
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASEDIR, TEST_DB)
            self.app = app.test_client()
            db.drop_all()
            db.create_all()

        self.assertEquals(app.debug, False)

    def tearDown(self):
        pass

    def register(self, name, email, password, confirm):
        return self.app.post('/register',data=dict(name=name, email=email, password=password, confirm=confirm), follow_redirects=True)

    def login(self, email, password):
        return self.app.post('/login', data=dict(email=email, password=password), follow_redirects=True)

    def register_user(self):
        self.app.get('/register', follow_redirects=True)
        self.register('esther', 'estherjsuh@gmail.com', 'HelloGoodbye', 'HelloGoodbye')

    def login_user(self):
        self.app.get('/login', follow_redirects=True)
        self.login('estherjsuh@gmail.com', 'HelloGoodbye')

    def logout_user(self):
        self.app.get('/logout', follow_redirects=True)

    def add_plants(self):
        self.register_user()
        self.login_user()
        user1 = User.query.filter_by(email='estherjsuh@gmail.com').first()
        plant1 = Plants(user1.user_id, 'aloe', 'good for burns', 9, 'aloe.jpg', '/static/img/aloe.jpg')
        plant2 = Plants(user1.user_id, 'fiddle', 'cannot stand wind', 7, 'fiddle.jpg', '/static/img/fiddle.jpg')
        plant3 = Plants(user1.user_id, 'lucky', 'money plant', 7, 'money.jpg', '/static/img/money.jpg')
        db.session.add(plant1)
        db.session.add(plant2)
        db.session.add(plant3)
        db.session.commit()

##TESTS##

    #TEST 1: this is to check if registration page comes up correctly with the Get request
    def test_user_registration_form_displays(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register Your New Account', response.data)

    #TEST 2: check if user registration works
    def test_valid_user_registration(self):
        #self.app.get('/register')#, follow_redirects=True)
        response = self.register('Esther', 'estherjsuh@gmail.com', 'ThisIsATest', 'ThisIsATest')
        self.assertIn(b'Registration Success!',response.data)

    #TEST 3: check if email duplication raises error
    def test_duplicate_email_error(self):
        self.app.get('/register', follow_redirects=True)
        self.register('Raccoon', 'estherjsuh@gmail.com', 'HelloGoodbye', 'HelloGoodbye')
        self.app.get('/register', follow_redirects=True)
        response = self.register('Raccoon', 'estherjsuh@gmail.com', 'HelloGoodbye', 'HelloGoodbye')
        self.assertIn(b'Email estherjsuh@gmail.com already exists', response.data)

    #TEST 4: check if registering with 2 different passwords raises error
    def test_mismatch_passwords(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('Raccoon', 'estherjsuh@gmail.com', 'HelloGoodbye', 'GoodbyeHello')
        self.assertIn(b'Field must be equal to password.', response.data)

    #TEST 5: check if incomplete form causes an error
    def test_missing_field_error(self):
        self.app.get('/register', follow_redirects=True)
        response= self.register('Esther', 'estherjsuh@mgmail.com', 'HelloGoodbye', '')
        self.assertIn(b'This field is required.', response.data)

    #TEST 6: check if login pages loads correctly
    def test_login_form_displays(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login To Your Account', response.data)

    #TEST 7: check if login is successful after registration
    def test_valid_login(self):
        self.app.get('/register', follow_redirects=True)
        self.register('Raccoon', 'estherjsuh@gmail.com', 'HelloGoodbye', 'HelloGoodbye')
        self.app.get('/login', follow_redirects=True)
        response = self.login('estherjsuh@gmail.com', 'HelloGoodbye')
        self.assertIn(b'Thanks for logging in Raccoon', response.data)

    #TEST 8: check if incorrect password raises error
    def test_invalid_login(self):
        self.app.get('/register', follow_redirects=True)
        self.register('Raccoon', 'estherjsuh@gmail.com', 'HelloGoodbye', 'HelloGoodbye')
        self.app.get('/login', follow_redirects=True)
        response = self.login('estherjsuh@gmail.com', 'GoodbyeHello')
        self.assertIn(b'Invalid login credentials', response.data)

    #TEST 9: check if logout works when user is logged in
    def test_valid_logout(self):
        self.app.get('/register', follow_redirects=True)
        self.register('Esther', 'estherjsuh@gmail.com', 'HelloGoodbye', 'HelloGoodbye')
        self.login('estherjsuh@gmail.com', 'HelloGoodbye')
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'Goodbye!',response.data)

    #TEST 10: check if invalid logout loads login page
    def test_invalid_logout(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'Login To Your Account', response.data)

    #TEST 11: check if myplants page shows when users register and login
    def test_myplants_page(self):
        self.register_user()
        self.login_user()
        response = self.app.get('/plants', follow_redirects=True)
        self.assertIn(b'Here Are Your Plants', response.data)

    #TEST 12: check that plants are added
    def test_add_plants_page(self):
        self.register_user()
        self.login_user()
        self.add_plants()
        response = self.app.get('/plants', follow_redirects=True)
        self.assertIn(b'Aloe', response.data)
        self.assertIn(b'Fiddle', response.data)
        self.assertIn(b'Lucky', response.data)

    #TEST 13:
    def test_add_plants_page_without_login(self):
        response = self.app.get('/new', follow_redirects=True)
        self.assertIn(b'Login To Your Account', response.data)



if __name__=='__main__':
    unittest.main()
