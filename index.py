from flask import Flask, render_template, request, redirect, url_for
from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql

app = Flask(__name__)

# initialize Connector object
connector = Connector()

# function to return the database connection
def getConnCreation() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "boxwood-valve-365621:us-west1:quizstorage",
        "pymysql",
        user="quizstorage",
        password="password",
        db="quizzes"
    )

    return conn

def getQuiz():
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getConnCreation,
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
        creator=getConnCreation,
    )

    with pool.connect() as db_conn:
        insert_stmt = sqlalchemy.text(
        "INSERT INTO quizzes (username, quiz) values (:username, :quiz)",
        )
        db_conn.execute(insert_stmt, username="DanTest", quiz=send_quiz)
    connector.close()

# create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getConnCreation,
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
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


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)