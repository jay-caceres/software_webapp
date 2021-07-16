from flask import Flask, render_template,url_for,request,flash,redirect, session
from forms import RegistrationForm,LoginForm,RegisterForm,FuelQuoteForm
from flask_login import login_user
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SECRET_KEY']='df0a82e89698f516dd362744546b8e96'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#db = SQLAlchemy(app)

quote =  (("10", "4800 Calhoun Rd", "07/16/2021", "1.50", "200.00"), )

@app.route('/login')
@app.route('/', methods=["GET", "POST"])
def home():
    #if request.method == "POST":
        #user = request.form.get("username")
        #return user
    form = LoginForm() #delete META after testing!!!
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'admin':
            flash('You have been logged in!', 'success')
            session['logged_in'] = True #connect back end.. eventually use database
            return redirect(url_for('Management'))
        else:
            flash("Login Unsuccessful. Please check username and password", 'danger')
            return redirect(url_for('home'))
    return render_template('home.html',form=form)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out!', 'danger')    
    return redirect(url_for('home'))

@app.route('/register', methods=["GET", "POST"])
def register():
    #if request.method == "POST":
        #user = request.form.get("username")
        #return user
    form = RegistrationForm()
    
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        
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



if __name__ == '__main__':
    app.run(debug=True)


