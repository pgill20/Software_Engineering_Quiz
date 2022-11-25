import sqlalchemy
import pymysql
from google.cloud.sql.connector import Connector
import json


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

def insertQuiz(send_quiz, timer):
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )
    quiz_list = send_quiz[0]
    testName = send_quiz[2]
    employer_e = send_quiz[1]

    quiz_q = json.dumps(quiz_list)

    with pool.connect() as db_conn:
        insert_stmt = sqlalchemy.text(
        "INSERT INTO quizzes (username, Test, quizQuestions, Employer, time) values (:username, :Test, :quizQuestions, :Employer, :time)",
        )
        db_conn.execute(insert_stmt, username="DanTest", Test=testName, quizQuestions=quiz_q, Employer=employer_e, time=timer)
    connector.close()

def getTestID(timer):
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )

    base_query = """
    SELECT testID FROM quizzes WHERE time='{time}'
    """
    query = base_query.format(time=timer)

    with pool.connect() as db_conn:
        testid = db_conn.execute(query).fetchall()
        return testid
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