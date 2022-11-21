from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql

# initialize Connector object
connector = Connector()

# function to return the database connection
def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "capstone-367716:us-west1:capstone",
        "pymysql",
        user="peelet",
        password="467Ranking",
        db="467captstone"
    )
    return conn

def getRankingsByTestID(testId):

    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )
    base_query = """
    SELECT * FROM rankings WHERE TestID='{id}'
    """
    query = base_query.format(id=testId)

    with pool.connect() as db_conn:
        result = db_conn.execute(query).fetchall()
        print(result)
        return result
    connector.close()

def insertTestResults(fullName, email, test, score, testId, employer):
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )
    base_query = """
    INSERT INTO rankings (FullName , Email , Test , Score , TestId , Employer) values ('{FullName}' , '{Email}' , '{Test}' , '{Score}' , '{TestId}' , '{Employer}')
    """
    query = base_query.format(FullName=fullName, Email=email, Test=test, Score=score, TestId=testId, Employer=employer)
    
    with pool.connect() as db_conn:
        db_conn.execute(query)
    connector.close()

def createQuiz(username, test, quizQuestions, employer, time):
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )
    base_query = """
    INSERT INTO quizzes (username , Test , quizQuestions, Employer, time) values ('{Username}' , '{Test}' , '{QuizQuestions}' , '{Employer}' , '{Time}')
    """
    query = base_query.format(Username=username, Test=test, QuizQuestions=quizQuestions, Employer=employer, Time=time)
    
    with pool.connect() as db_conn:
        db_conn.execute(query)
    connector.close()

# createQuiz('john daly', 'swe new grad', '[(1,b), (2,c)]', 'Google', '7:45am')


# insertTestResults("John ", "john@oregon.edu", "Test 1", 36, "ID 255", "Google")
# getRankingsByTestID('ID 255')

# createQuiz('john daly', 'swe new grad', '[(1,b), (2,c)]', 'Google', '7:45am')


# INSERT INTO rankings (FullName , Email , Test , Score , TestId , Employer) values ("Troy Peele 2", "peelet@oregonstate.edu", "Test 1", 11, "ID 255", "Google");
# getRankingsByTestID('ID 255')

# CREATE TABLE quizzes (username varchar(255), Test varchar(255), quizQuestions varchar(800), Employer varchar(255), time varchar(255), testID INT NOT NULL AUTO_INCREMENT, PRIMARY KEY(testId));