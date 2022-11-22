# API KEY MUST STAY PRIVATE, IF POSTED ONLINE OR IN A CHAT, EMAIL WILL BE DISABLED
SENDGRID_API = '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' 

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
def sendEmail(email, subjectInfo, testLink):
    message = Mail(
        from_email="peelet@oregonstate.edu",
        to_emails=email,
        subject=subjectInfo,
        html_content='<strong> You have been invited to take a timed test. Please use this link to start ' + testLink + ' </strong>')
    try:
        sg = SendGridAPIClient(SENDGRID_API)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

# example of utilizing function below
# sendEmail('ltcharger@yahoo.com','Invite to test', 'google.com')