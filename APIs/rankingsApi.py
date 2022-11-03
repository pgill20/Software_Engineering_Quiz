from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql

# initialize Connector object
connector = Connector()

# function to return the database connection
def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "boxwood-valve-365621:us-west1:rankings",
        "pymysql",
        user="peelet",
        password="467Ranking",
        db="ranking"
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
        insert_stmt = sqlalchemy.text(
        "INSERT INTO entries (guestName, content) values (:guestName, :content)",
        )
        db_conn.execute(query)
    connector.close()

# insertTestResults("Troy ", "peelet@oregon.edu", "Test 1", 8, "ID 255", "Google")

# CREATE TABLE rankings (FullName varchar(255), Email varchar(255), Test varchar(255), Score int, TestId varchar(255), Employer varchar(255), rankingID INT NOT NULL AUTO_INCREMENT, PRIMARY KEY(rankingID));

# INSERT INTO rankings (FullName , Email , Test , Score , TestId , Employer) values ("Troy Peele", "peelet@oregonstate.edu", "Test 1", 10, "ID 255", "Google");