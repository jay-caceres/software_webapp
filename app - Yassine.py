from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/Registration")
def Registration():
    return render_template('Registration.html')

@app.route("/Management")
def Management():
    return render_template('Management.html')


if __name__ == '__main__':
    app.run(debug=True)