from flask import Flask, render_template,url_for,request,flash,redirect
from forms import RegistrationForm,LoginForm
app = Flask(__name__)

app.config['SECRET_KEY']='df0a82e89698f516dd362744546b8e96'

@app.route('/login')
@app.route('/', methods=["GET", "POST"])
def home():
    #if request.method == "POST":
        #user = request.form.get("username")
        #return user
    form2 = LoginForm()
    
    
    return render_template('home.html',form=form2)

@app.route('/register', methods=["GET", "POST"])
def register():
    #if request.method == "POST":
        #user = request.form.get("username")
        #return user
    form1 = RegistrationForm()
    
    if form1.validate_on_submit():
        flash(f'Account created for {form1.username.data}!','success')
        
        return redirect(url_for('home'))
    return render_template('register_user.html',form=form1)


@app.route("/fuelQuote")
def fuelQuote():
    return render_template('fuelQuote.html')

@app.route("/history")
def history():
    return render_template('history.html')

@app.route("/Registration")
def Registration():
    return render_template('Registration.html')

@app.route("/Management")
def Management():
    return render_template('Management.html')



if __name__ == '__main__':
    app.run(debug=True)


