
from webapp.forms import LoginForm
from webapp import db, bcrypt, app as appy
from webapp.models import User
import unittest
from flask_testing import TestCase
from flask import Flask, request
import datetime

appy.config['TESTING'] = True
appy.config['WTF_CSRF_ENABLED'] = False


class FlaskTestCase(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True
    def create_app(self):

        app = Flask(__name__)
        
        db.init_app(app)
        return appy
    # Ensure that Flask was set up correctly

    def setUp(self):

        db.create_all()

    def login(self, username, password):
        return self.client.post('/', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

    def test_index(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_invalid_password(self): 
        #app.config['WTF_CSRF_ENABLED'] = False
        response = self.client.post(
            '/',
            data=dict(username="admin", password="1"),
            follow_redirects=True
        )
        self.assertIn(b'Login Unsuccessful. Please check username and password', response.data)
    
    def test_valid_registration(self):   
        response = self.client.post('/register',data=dict(username="admin", password="admin", confirm_password="admin"),follow_redirects=True)
        self.assertIn(b'Account created for',response.data)

    def test_valid_information_registration(self):
        response = self.client.post('/Registration',data=dict(fullname="Jane Doe", address1="1234 Street Road", address2="", city="Houston", state="TX", zipcode="77469"), follow_redirects=True)
        self.assertIn(b'Information registered',response.data)

    def test_user_indb(self):
        user = User(username='admin', password='admin')
        db.session.add(user)
        db.session.commit()
        assert user in db.session


    def test_login(self):
        user = User(username='admin_test', password=bcrypt.generate_password_hash('admin').decode('utf-8'))
        db.session.add(user)
        db.session.commit()
        rv = self.login('admin_test','admin')

        self.assertIn(b'You have been logged in!', rv.data)


    def test_logout(self):
        self.client.post('/',data={
                    'username': 'admin',
                    'password': 'admin'
                }, follow_redirects = True)
        response = self.client.get('/logout',follow_redirects=True)
        self.assertIn(b'You have been logged out!',response.data)
    #REGISTER

    def test_username_register_invalid(self):
        response = self.client.post('/register',data=dict(username="a", password="1", confirm_password="1"),follow_redirects=True)
        self.assertIn(b'Field must be between 2 and 20 characters long.',response.data)

    def test_password_register_invalid(self):   
        response = self.client.post('/register',data=dict(username="admin", password="1", confirm_password="2"),follow_redirects=True)
        self.assertIn(b'Field must be equal to password.',response.data)

    
    #INFORMATION REGISTRATION
   

    def test_valid_get_quote_form(self):        
        self.client.post('/Registration',data=dict(fullname="Jane Doe", address1="1234 Street Road", address2="", city="Houston", state="TX", zipcode="77469"), follow_redirects=True)

        response = self.client.post('/fuelQuote',data=dict(gallons_requested=3,delivery_date=datetime.date(2021, 9, 10), get_quote=True), follow_redirects=True)
        self.assertIn(b'Quote',response.data)

    def test_valid_quote_form(self):        
        self.client.post('/Registration',data=dict(fullname="Jane Doe", address1="1234 Street Road", address2="", city="Houston", state="TX", zipcode="77469"), follow_redirects=True)
        self.client.post('/fuelQuote',data=dict(gallons_requested=3,delivery_date=datetime.date(2021, 9, 10), get_quote=True), follow_redirects=True)
        response = self.client.post('/fuelQuote',data=dict(gallons_requested=3,delivery_date=datetime.date(2021, 9, 10), price = 1,total=2,submit=True), follow_redirects=True)
        self.assertIn(b'Quote Received Successfully!',response.data)

    def tearDown(self): 

        db.session.remove()
        db.drop_all()
        db.create_all()


if __name__ == '__main__':
    unittest.main()