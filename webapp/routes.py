from enum import unique
from flask import Flask, render_template,url_for,request,flash,redirect, session
from webapp import app, db, bcrypt
from webapp.forms import RegistrationForm,LoginForm,RegisterForm,FuelQuoteForm
from flask_login import login_user, current_user, logout_user
from webapp.models import User, Registered_user, Fuel_quote

userid = 0

@app.route('/login')
@app.route('/', methods=["GET", "POST"])
def home():
    #if request.method == "POST":
        #user = request.form.get("username")
        #return user
    form = LoginForm() #delete META after testing!!!
    if current_user.is_authenticated:
        return redirect(url_for('Management'))
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            global userid
            userid=user.id
            login_user(user) #remember=form.remember.data
            flash('You have been logged in!', 'success')
            return redirect(url_for('Management'))
        else:
            flash("Login Unsuccessful. Please check username and password", 'danger')
            return redirect(url_for('home'))
    return render_template('home.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!', 'danger')    
    return redirect(url_for('home'))

@app.route('/register', methods=["GET", "POST"])
def register():
    #if request.method == "POST":
        #user = request.form.get("username")
        #return user
    if current_user.is_authenticated:
        return redirect(url_for('Management'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You can now login','success')
        return redirect(url_for('home'))
    return render_template('register_user.html',form=form)


@app.route("/fuelQuote", methods=['GET', 'POST'])
def fuelQuote():
    client =Registered_user.query.all()
    deliveryAddress = Registered_user.query.get(1).address1
    form = FuelQuoteForm()
    if form.validate_on_submit():
        quote = Fuel_quote(number_of_gallons=form.gallons_requested.data, delivery_address = deliveryAddress, 
                    delivery_date = form.delivery_date.data, price_per_gallon = 3, total = 0, user_id = 1)
        db.session.add(quote)
        db.session.commit()
        flash(f'Quote Received Successfully!', 'success')
        return redirect(url_for('Management'))
    return render_template('fuelQuote.html', form=form)

@app.route("/history")
def history():
    quote = Fuel_quote.query.all()
    return render_template('history.html',quote=quote)

@app.route("/Registration",methods=["GET", "POST"])
def Registration():
    form = RegisterForm()
    if form.validate_on_submit():
        registered_user = Registered_user.query.filter_by(user_id=userid).first()
        if registered_user is None:
            registered_user = Registered_user(user_id=userid, fullname=form.fullname.data, address1=form.address1.data, address2=form.address2.data, city=form.city.data, state=form.state.data, zipcode=form.zipcode.data)
            db.session.add(registered_user)
            db.session.commit()
        else:
            registered_user.fullname = form.fullname.data
            registered_user.address1 = form.address1.data
            registered_user.address2 = form.address2.data
            registered_user.city = form.city.data
            registered_user.state = form.state.data
            registered_user.zipcode = form.zipcode.data
            db.session.commit()
        flash(f'Information registered','success')
        return redirect(url_for('Management'))
    return render_template('Registration.html', form=form)
    

@app.route("/Management", methods=["GET", "POST"])
def Management():

    registered_user = Registered_user.query.filter_by(user_id=userid).first()
    print(userid)
    table_values=registered_user
    if table_values is None:
        data = (
            ('', '', '', '', '', '')
        )
    else:
        data = (
        (table_values.fullname, table_values.address1, table_values.address2, table_values.city, table_values.state, table_values.zipcode)
        )



    return render_template('Management.html', data=data)