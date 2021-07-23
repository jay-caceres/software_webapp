from webapp import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    registered = db.relationship('Registered_user',uselist=False, backref='user')
    fuel_form_quote = db.relationship('Fuel_quote', backref='quote',lazy=True)
     
    
    def __repr__(self):
        return f"User('{self.username}')"


class Registered_user(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id') ,nullable=False,primary_key=True)
    fullname = db.Column(db.String(30), nullable=False)
    address1 = db.Column(db.String(120), nullable=False) #whoever is incharge of this part can split address to address1/address2
    address2 = db.Column(db.String(120))
    city = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Registered_user('{self.fullname}')"

class Fuel_quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number_of_gallons = db.Column(db.Integer,nullable = False)
    delivery_address= db.Column(db.String(120),db.ForeignKey('registered_user.address1'), nullable = False)
    delivery_date = db.Column(db.Date, nullable=False)
    price_per_gallon=db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id') ,nullable=False)

    def __repr__(self):
        return f"fuel_quote('{self.user_id}','{self.number_of_gallons}','{self.delivery_address}','{self.total}')"

#maybe make a history table/class so once a user makes a purchase,
#  that history table is populated and when calculating the rate 
# we can see if that user has a history or not  