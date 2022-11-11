from flask import Flask, render_template, request, redirect
from db_connector import connect_to_database, execute_query

app = Flask(__name__)


# @app.route('/')
# def index():
#     db_connection = connect_to_database()
#     query = "SELECT participant_id, first_name, password FROM Participants;"
#     result = execute_query(db_connection, query).fetchall()
#     return render_template('index.html', rows=result)


# @app.route('/login')
# def login():
#     return render_template('login.html')

@app.route('/')
def index():
    return 'Web App with Python Flask!'


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
