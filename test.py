
from forms import LoginForm
from webapp import app
import unittest
from flask_testing import TestCase
from flask import Flask, request
import datetime


app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
class FlaskTestCase(TestCase):
    def create_app(self):

        app = Flask(__name__)
    
        return app
    # Ensure that Flask was set up correctly

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_invalid_password(self): 
        #app.config['WTF_CSRF_ENABLED'] = False
        tester = app.test_client(self)
        response = tester.post(
            '/',
            data=dict(username="admin", password="1"),
            follow_redirects=True
        )
        self.assertIn(b'Login Unsuccessful. Please check username and password', response.data)


    def test_login(self): 
        tester = app.test_client(self)
        response = tester.post('/',data={
                    'username': "admin",
                    'password': "admin"
                }, follow_redirects = True)
        self.assertIn(b'You have been logged in!', response.data)


    def test_logout(self):
        tester = app.test_client(self)
        tester.post('/',data={
                    'username': 'admin',
                    'password': 'admin'
                }, follow_redirects = True)
        response = tester.get('/logout',follow_redirects=True)
        self.assertIn(b'You have been logged out!',response.data)
    #REGISTER

    def test_username_register_invalid(self):
        tester = app.test_client(self)
        response = tester.post('/register',data=dict(username="a", password="1", confirm_password="1"),follow_redirects=True)
        self.assertIn(b'Field must be between 2 and 20 characters long.',response.data)

    def test_password_register_invalid(self):   
        tester = app.test_client(self)
        response = tester.post('/register',data=dict(username="admin", password="1", confirm_password="2"),follow_redirects=True)
        self.assertIn(b'Field must be equal to password.',response.data)

    def test_valid_registration(self):   
        tester = app.test_client(self)
        response = tester.post('/register',data=dict(username="admin", password="admin", confirm_password="admin"),follow_redirects=True)
        self.assertIn(b'Account created for',response.data)
    #INFORMATION REGISTRATION
   

    def test_valid_information_registration(self):
        tester = app.test_client(self)
        response = tester.post('/Registration',data=dict(fullname="Jane Doe", address1="1234 Street Road", address2="", city="Houston", state="TX", zipcode="77469"), follow_redirects=True)
        self.assertIn(b'Information registered',response.data)

    def test_valid_quote_form(self):
        tester = app.test_client(self)
        response = tester.post('/fuelQuote',data=dict(gallons_requested=3,delivery_date=datetime.date(2020, 1, 1)), follow_redirects=True)
        self.assertIn(b'Quote Received Successfully!',response.data)


if __name__ == '__main__':
    unittest.main()