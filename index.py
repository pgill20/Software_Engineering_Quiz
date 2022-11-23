from flask import Flask, render_template, request, redirect, url_for
from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql
import datetime
import json
# from db_connector import connect_to_database, execute_query
from APIs import rankingsApi
from sendemail import sendEmail
from quizAPI import *

app = Flask(__name__)

# @app.route('/')
# def index():
# #     db_connection = connect_to_database()
# #     query = "SELECT participant_id, first_name, password FROM Participants;"
# #     result = execute_query(db_connection, query).fetchall()
#     return render_template('index.html')

# @app.route('/')
# def login():
#     return render_template('login.html')


# @app.route('/register', methods=['POST', 'GET'])
    # db_connection = connect_to_database()
    # if request.method == 'POST':
    #     first_name = request.form['first_name']
    #     last_name = request.form['last_name']
    #     password = request.form['password']
    #     query = "INSERT INTO Participants (first_name, last_name, password) VALUES (%s, %s, %s);"
    #     data = (first_name, last_name, password)
    #     execute_query(db_connection, query, data)
    #     return redirect('/index')

@app.route('/create_quiz')
def create_quiz():
    # This route will allow employers to create their quiz. 
    return render_template('create_quiz.html')

@app.route('/submit_quiz', methods=["POST"])
def submit_quiz():
    # This route is taken from create_quiz and allows created quizzes to be submitted to the database.
    json_input = json.loads(request.data)
    quiz = json_input[0]
    employer = json_input[1]
    testName = json_input[2]
    email = json_input[3]
    subjectInfo = employer + " has invited you to take a test: " + testName
    timer = datetime.datetime.now()
    insertQuiz(json_input, timer)
    testID = getTestID(timer)
    sendEmail(email, subjectInfo, testID)
    return redirect(url_for('index'), code=302)

@app.route('/quiz')
def take_quiz():
    # This route is taken from an email link to a particular quiz
    if not request.args:
        return "You cannot access this page directly. Please access this page through an email link from your potential employer."
    group = pullQuestions(request.args)
    quiz = group[0][0]
    employer = group[0][1]
    testid = request.args.get('testid')
    #quiz = [["multipleChoice", "question", "A", "B", "C", "D"]]
    #employer = "Dan"
    return render_template('take_quiz.html', q=quiz, t=testid, e=employer)

@app.route('/submit_quiz_answers', methods=["POST"])
def submit_quiz_answers():
    # This route is taken from take_quiz and allows quiz scores and data to be submitted to the rankings database.
    data = json.loads(request.data)
    print(data)
    fullName = data["fullName"]
    email = data["email"]
    score = data["score"]
    testid = data["testid"]
    employer = data["employer"]
    insertTestResults(fullName, email, score, testid, employer)
    return redirect(url_for('index'), code=302)

@app.route('/')
def index():
    return "homepage for the Engineer"


@app.route('/rankings')
def table():
    headings = ["Full Name" , "Email" , "Test" , "Score" , "Test ID" , "Employer", "Applicant ID"]
    index = 3

    # NEED TO UTILIZE A TEST ID FOR GAINING INFORMATION
    rankingData = rankingsApi.getRankingsByTestID("ID 255")
    rankingData.sort(key = lambda x: x[index], reverse=True)
    return render_template("table.html", headings=headings, data=rankingData)

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)

# @app.route('/login')
# def login():
#     return render_template('login.html')


# @app.route('/register', methods=['POST', 'GET'])
# def register():
#     db_connection = connect_to_database()
#     if request.method == 'POST':
#         first_name = request.form['first_name']
#         last_name = request.form['last_name']
#         password = request.form['password']
#         query = "INSERT INTO Participants (first_name, last_name, password) VALUES (%s, %s, %s);"
#         data = (first_name, last_name, password)
#         execute_query(db_connection, query, data)
#         return redirect('/index')


    # elif request.method == 'GET':
    # Under Construction


