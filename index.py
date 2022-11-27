from flask import Flask, render_template, request, redirect, session, url_for
from google.cloud.sql.connector import Connector
import datetime
import json
from APIs import rankingsApi
from sendemail import sendEmail
from quizAPI import *
import logging
import time

# For User Authentication
from os import environ as env
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)

# Controllers API

@app.route("/")
def index():
    if session:
        app.logger.info(session.get('user').get('userinfo').get('email'))
    return render_template(
        "index.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("index", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


@app.route('/create_quiz')
def create_quiz():
    # This route will allow employers to create their quiz. 
    return render_template('create_quiz.html', session=session.get("user"))


@app.route('/submit_quiz', methods=["POST"])
def submit_quiz():
    # This route is taken from create_quiz and allows created quizzes to be submitted to the database.
    json_input = json.loads(request.data)

    employer = json_input[1]
    testName = json_input[2]
    email = json_input[3]
    user = session.get('user').get('userinfo').get('nickname')

    subjectInfo = employer + " has invited you to take a test: " + testName
    timer = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    app.logger.info("Inserting test and retrieving testID...")
    testID = insertQuiz(json_input, timer, user)
    app.logger.info("Quiz successfully uploaded to database. ID retrieved.")
    app.logger.info("Sending email to " + email + "...")
    testLink = "https://softwarequizcapstone.herokuapp.com/quiz?testid=" + str(testID[0][0])
    sendEmail(email, subjectInfo, testLink)
    app.logger.info("Email successfully sent to candidate.")
    return redirect(url_for('index'), code=302)


@app.route('/quiz')
def take_quiz():
    # This route is taken from an email link to a particular quiz
    if not request.args:
        return "You cannot access this page directly. Please access this page through an email link from your potential employer."
    group = pullQuestions(request.args)
    quiz = group[0][0]
    employer = group[0][1]
    testName = group[0][2]
    testid = request.args.get('testid')
    #quiz = [["multipleChoice", "question", "A", "B", "C", "D"]]
    #employer = "Dan"
    return render_template('take_quiz.html', q=quiz, t=testid, e=employer, n=testName)


@app.route('/submit_quiz_answers', methods=["POST"])
def submit_quiz_answers():
    # This route is taken from take_quiz and allows quiz scores and data to be submitted to the rankings database.
    data = json.loads(request.data)
    print(data)
    fullName = data["fullName"]
    email = data["email"]
    score = data["score"]
    testid = data["testid"]
    employer = session.get('user').get('userinfo').get('email')
    testName = data["testName"]
    insertTestResults(fullName, email, score, testid, employer, testName)
    return redirect(url_for('index'), code=302)


@app.route('/rankings')
def table():
    user = session.get('user')
    employerName = user["userinfo"]["email"]
    # employerName = "john@google.com"

    headings = ["Full Name", "Email", "Test", "Score"]
    index = 3

    # NEED TO UTILIZE A TEST ID FOR GAINING INFORMATION
    rankingData = rankingsApi.getRankingsByEmployerName(employerName)
    rankingData.sort(key=lambda x: x[index], reverse=True)
    return render_template("table.html", headings=headings, data=rankingData, session=session.get("user"))


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
