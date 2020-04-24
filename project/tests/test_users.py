import os
import unittest

from project import app, db

TEST_DB ='users.db'


class UsersTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        self.assertEquals(app.debug, False)

    def tearDown(self):
        pass

    def register(self, name, email, password, confirm):
        return self.app.post('/register',data=dict(name=name, email=email, password=password, confirm=confirm), follow_redirects=True)

    #this is to check if registration page comes up correctly with the Get request
    def test_user_registration_form_displays(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register Your New Account', response.data)

    #check if user registration works
    def test_valid_user_registration(self):
        #self.app.get('/register')#, follow_redirects=True)
        response = self.register('Esther', 'estherjsuh@gmail.com', 'ThisIsATest', 'ThisIsATest')
        self.assertIn(b'Registration Success!',response.data)

    #check if email duplication raises error
    def test_duplicate_email_error(self):
        self.app.get('/register', follow_redirects=True)
        self.register('Raccoon', 'estherjsuh@gmail.com', 'HelloGoodbye', 'HelloGoodbye')
        self.app.get('/register', follow_redirects=True)
        response = self.register('Raccoon', 'estherjsuh@gmail.com', 'HelloGoodbye', 'HelloGoodbye')
        self.assertIn(b'Email estherjsuh@gmail.com already exists', response.data)

    #check if incomplete form causes an error
    def test_missing_field_error(self):
        self.app.get('/register', follow_redirects=True)
        response= self.register('Esther', 'estherjsuh@mgmail.com', 'HelloGoodbye', '')
        self.assertIn(b'This field is required.', response.data)

if __name__=='__main__':
    unittest.main()
