from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql

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

def getRankingsByTestID(testId):

    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )
    base_query = """
    SELECT FullName, Email, testName, Score FROM rankings WHERE TestID='{id}'
    """
    query = base_query.format(id=testId)

    with pool.connect() as db_conn:
        result = db_conn.execute(query).fetchall()
        print(result)
        return result
    connector.close()

def getRankingsByEmployerName(employer):

    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )
    base_query = """
    SELECT FullName, Email, testName, Score FROM rankings WHERE Employer='{name}'
    """
    query = base_query.format(name=employer)

    with pool.connect() as db_conn:
        result = db_conn.execute(query).fetchall()
        print(result)
        return result
    connector.close()

def insertTestResults(fullName, email, testName, score, testId, employer):
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )
    base_query = """
    INSERT INTO rankings (FullName , Email , testName , Score , TestId , Employer) values ('{FullName}' , '{Email}' , '{testName}' , '{Score}' , '{TestId}' , '{Employer}')
    """
    query = base_query.format(FullName=fullName, Email=email, testName=testName, Score=score, TestId=testId, Employer=employer)
    
    with pool.connect() as db_conn:
        db_conn.execute(query)
    connector.close()

def createQuiz(username, test, TestName, quizQuestions, employer, time):
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )
    base_query = """
    INSERT INTO quizzes (username , Test , TestName, quizQuestions, Employer, time) values ('{Username}' , '{Test}' , '{TestName}', '{QuizQuestions}' , '{Employer}' , '{Time}')
    """
    query = base_query.format(Username=username, Test=test, QuizQuestions=quizQuestions, Employer=employer, Time=time)
    
    with pool.connect() as db_conn:
        db_conn.execute(query)
    connector.close()

# SAMPLE TEST RESULT INSERTION & VALIDATION
# insertTestResults("Troy Peele 2", "peelet@oregonstate.edu", "Test 1", 11, "ID 255", "Google");
# getRankingsByTestID('ID 255')
# getRankingsByEmployerName("john@google.com")
