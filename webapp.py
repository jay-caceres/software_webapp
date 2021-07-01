from flask import Flask, render_template,url_for,request
app = Flask(__name__)


@app.route('/login')
@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user = request.form.get("username")
        return user
    return render_template('home.html')

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


