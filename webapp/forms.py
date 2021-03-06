
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField,IntegerField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo,NumberRange,Optional,ValidationError
from wtforms.fields.html5 import DateField
from webapp.models import User, Registered_user
from wtforms_components import DateRange
from datetime import date

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    #submit = SubmitField('Submit')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    #submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    fullname = StringField('fullname', validators=[DataRequired(),Length(min=2, max=50)])
    address1 = StringField('address1', validators=[DataRequired(),Length(max=100)])
    address2 = StringField('address2', validators=[Length(max=100)])
    city = StringField('city', validators=[DataRequired(),Length(max=100)])
    state = SelectField('state', choices=states, validators=[DataRequired()])
    zipcode = StringField('zipcode', validators=[DataRequired(),Length(min=5, max=9)])

class FuelQuoteForm(FlaskForm):
    #temp = Registered_user.query.get(1).address1
    gallons_requested = IntegerField('Gallons Requested', 
                        validators=[DataRequired(),NumberRange(min=0, message='Gallons need to be positive')])
    delivery_address = StringField('Delivery Address',default='', validators = [Optional()],render_kw={'readonly': True})
    delivery_date = DateField('Delivery Date',validators=[DataRequired(), DateRange(min=date.today())])
    price = DecimalField('Suggested Price/Gallon',validators = [Optional()] ,render_kw={'readonly': True})
    total = DecimalField("Total Amount Due", validators = [Optional()],render_kw={'readonly': True})
    #NEW 
    get_quote = SubmitField("Get Quote")
    submit = SubmitField("Submit Quote")