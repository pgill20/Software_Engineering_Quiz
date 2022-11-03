from flask import Flask, render_template, request, redirect
# from db_connector import connect_to_database, execute_query
# from APIs import rankingsApi

app = Flask(__name__)


@app.route('/')
def index():
    db_connection = connect_to_database()
    query = "SELECT participant_id, first_name, password FROM Participants;"
    result = execute_query(db_connection, query).fetchall()
    return render_template('index.html')

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

    # elif request.method == 'GET':
    # Under Construction


@app.route('/rankings')
def table():
    headings = ["Full Name" , "Email" , "Test" , "Score" , "Test ID" , "Employer", "Applicant ID"]
    index = 3
    # rankingData = rankingsApi.getRankingsByTestID("ID 255")
    rankingData = [
    ["John Daily", "jd@google.com", "A", "19", "Test 3A", "Google", "1"],
    ["Kevin Daily", "jacobd@google.com", "A", "28","Test 3A", "Google", "3"],
    ["Vicky Brown", "brownv@osu.com", "A", "22", "Test 3A", "Google", "2"]
    ]
    rankingData.sort(key = lambda x: x[index], reverse=True)
    return render_template("table.html", headings=headings, data=rankingData)
# app.run(host='0.0.0.0', port=81)