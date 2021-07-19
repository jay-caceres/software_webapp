from enum import unique
from flask import Flask, render_template,url_for,request,flash,redirect, session
from webapp import app, db, bcrypt
from webapp.forms import RegistrationForm,LoginForm,RegisterForm,FuelQuoteForm
from flask_login import login_user, current_user, logout_user
from webapp.models import User



quote =  (("10", "4800 Calhoun Rd", "07/16/2021", "1.50", "200.00"), )

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
    form = FuelQuoteForm()
    if form.validate_on_submit():
        flash(f'Quote Received Successfully!', 'success')
        return redirect(url_for('Management'))
    return render_template('fuelQuote.html', form=form)

@app.route("/history")
def history():
    return render_template('history.html',quote=quote)

@app.route("/Registration",methods=["GET", "POST"])
def Registration():
    form = RegisterForm()
    if form.validate_on_submit():
       
        flash(f'Information registered','success')
        return redirect(url_for('Management'))
    return render_template('Registration.html', form=form)
    

@app.route("/Management", methods=["GET", "POST"])
def Management():
    return render_template('Management.html')