from flask import Flask, render_template, request, redirect, url_for
from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql
import datetime
import json
from db_connector import connect_to_database, execute_query
from APIs import rankingsApi

app = Flask(__name__)

# initialize Connector object
connector = Connector()

# function to return the database connection
def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "test-capstone-project:us-west1:capstone-final",
        "pymysql",
        user="teamTriforce",
        password="467Ranking",
        db="capstone"
    )
    return conn

def getQuiz():
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )

    with pool.connect() as db_conn:
        result = db_conn.execute("SELECT * FROM quizzes").fetchall()
        for row in result:
            print(row)
        print("\n")    
    connector.close()

def insertQuiz(send_quiz):
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )

    with pool.connect() as db_conn:
        insert_stmt = sqlalchemy.text(
        "INSERT INTO quizzes (username, Test, quizQuestions, Employer, time) values (:username, :Test, :quiz, :employer, :time)",
        )
        db_conn.execute(insert_stmt, username="DanTest", Test="Test Test", quiz=send_quiz, employer="Dan's House of Quizzes", time=datetime.datetime())
    connector.close()

def pullQuestions(arg_dict):
    testid = arg_dict.get("testid")
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )

    with pool.connect() as db_conn:
        select_stmt = sqlalchemy.text(
            "SELECT quizQuestions, Employer FROM quizzes WHERE testid=:id"
        )
        quiz = db_conn.execute(select_stmt, id=testid)

        quiz = list(quiz)
        return quiz

def insertTestResults(fullName, email, score, testId, employer):
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )
    base_query = """
    INSERT INTO rankings (FullName , Email , Score , TestId , Employer) values ('{FullName}' , '{Email}' , '{Score}' , '{TestId}' , '{Employer}')
    """
    query = base_query.format(FullName=fullName, Email=email, Score=score, TestId=testId, Employer=employer)
   
    with pool.connect() as db_conn:
        db_conn.execute(query)
    connector.close()

# create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

# @app.route('/')
# def index():
#     db_connection = connect_to_database()
#     query = "SELECT participant_id, first_name, password FROM Participants;"
#     result = execute_query(db_connection, query).fetchall()
#     return render_template('index.html', rows=result)

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    # db_connection = connect_to_database()
    # if request.method == 'POST':
    #     first_name = request.form['first_name']
    #     last_name = request.form['last_name']
    #     password = request.form['password']
    #     query = "INSERT INTO Participants (first_name, last_name, password) VALUES (%s, %s, %s);"
    #     data = (first_name, last_name, password)
    #     execute_query(db_connection, query, data)
    #     return redirect('/index')
    return render_template('register.html')

@app.route('/create_quiz')
def create_quiz():
    # This route will allow employers to create their quiz. 
    return render_template('create_quiz.html')

@app.route('/submit_quiz', methods=["POST"])
def submit_quiz():
    # This route is taken from create_quiz and allows created quizzes to be submitted to the database.
    insertQuiz(request.data)
    return redirect(url_for('index'), code=302)

@app.route('/quiz')
def take_quiz():
    # This route is taken from an email link to a particular quiz
    if not request.args:
        return "You cannot access this page directly. Please access this page through an email link from your potential employer."
    #group = pullQuestions(request.args)
    #quiz = group[0][0]
    #employer = group[0][1]
    testid = request.args.get('testid')
    quiz = [["multipleChoice", "question", "A", "B", "C", "D"]]
    employer = "Dan"
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
def table():
    headings = ["Full Name" , "Email" , "Test" , "Score" , "Test ID" , "Employer", "Applicant ID"]
    index = 3
    # rankingData = rankingsApi.getRankingsByTestID("ID 255")
    rankingData = ["Troy ", "peelet@oregon.edu", "Test 1", "8", "ID 255", "Google"]
    rankingData.sort(key = lambda x: x[index])
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

