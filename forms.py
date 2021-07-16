
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField,IntegerField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo,NumberRange,Optional
from wtforms.fields.html5 import DateField


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    #submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    #submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    fullname = StringField('fullname', validators=[DataRequired(),Length(min=2, max=20)])
    address1 = StringField('address1', validators=[DataRequired()])
    address2 = StringField('address2')
    city = StringField('city', validators=[DataRequired()])
    state = SelectField('state', choices=states, validators=[DataRequired()])
    zipcode = StringField('zipcode', validators=[DataRequired()])

class FuelQuoteForm(FlaskForm):
    gallons_requested = IntegerField('Gallons Requested', 
                        validators=[DataRequired(),NumberRange(min=0, message='Gallons need to be positive')])
    delivery_address = StringField('Delivery Address', validators = [Optional()],render_kw={'readonly': True})
    delivery_date = DateField('Delivery Date',validators=[DataRequired()])
    price = DecimalField('Suggested Price/Gallon',validators = [Optional()] ,render_kw={'readonly': True})
    total = DecimalField("Total Amount Due", validators = [Optional()],render_kw={'readonly': True})
    submit = SubmitField("Calculate Total")