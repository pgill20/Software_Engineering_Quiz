SENDGRID_API = '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'

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
def sendEmail(email):
    message = Mail(
        from_email="peelet@oregonstate.edu",
        to_emails=email,
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

# def sendEmail(email):
#     sg = sendgrid.SendGridAPIClient(api_key='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')
#     from_email = Email("peelet@oregonstate.edu")
#     to_email = To("peelet@oregonstate.edu")
#     subject = "Sending with SendGrid is Fun"
#     content = Content("text/plain", "and easy to do anywhere, even with Python")
#     mail = Mail(from_email, to_email, subject, content)
#     response = sg.client.mail.send.post(request_body=mail.get())
#     print(response.status_code)
#     print(response.body)
#     print(response.headers)


# sendEmail('peelet@oregonstate.edu')
# sendEmail('ltcharger@yahoo.com')