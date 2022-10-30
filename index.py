from flask import Flask, render_template
from APIs import rankingsApi

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/rankings')
def table():
    headings = ["Full Name" , "Email" , "Test" , "Score" , "Test ID" , "Employer", "Applicant ID"]
    rankingData = rankingsApi.getRankingsByTestID("ID 255")
    return render_template("table.html", headings=headings, data=rankingData)


app.run(host='0.0.0.0', port=81)
