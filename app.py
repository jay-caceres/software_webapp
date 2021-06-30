from flask import Flask, render_template, url_for
app = Flask(__name__)


@app.route("/")
@app.route("/fuelQuote")
def fuelQuote():
    return render_template('fuelQuote.html')

@app.route("/history")
def history():
    return render_template('history.html')



