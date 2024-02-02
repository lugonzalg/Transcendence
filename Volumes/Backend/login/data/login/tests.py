from . import models
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from transcendence.settings import logger
from django.contrib.auth.hashers import make_password
from ninja import Schema

def get_user_by_email(email: str) -> models.user_login | None:

    try:
        print(f"email: {email}")
        db_user = models.user_login.objects.all()
        print(len(db_user))

        db_user = models.user_login.objects.filter(email=email).get()
        return db_user

    except ObjectDoesNotExist as err:
        logger.error(f"Error: Not Found {err}")

    except Exception as err:
        logger.error(f"Error: Unhandled {err}")

import smtplib
import base64

class Mail(Schema):

    sender: str
    receiver: str
    subject: str
    body: str
    message: str = None

    def _encode_image(self, src: str) -> str:

        try:
            with open(src, 'rb') as fd:
                encoded = base64.b64encode(fd.read())
                return encoded.decode('utf-8')

        except FileNotFoundError as err:
            logger.error(f"Error: File not found {err}")
        except Exception as err:
            logger.error(f"Error: Unhandled {err}")

        return None

    def build(self, otp_code: int = 1234):
        self.subject = "Your Verification Code"

    # Sample email body with OTP code
        body_text = f"""\
Dear User,

Your OTP is {otp_code}. This code is valid for 10 minutes.

Best regards,
[Your Company Name]
"""

        body_html = f"""\
<html>
  <head></head>
  <body>
    <p>Dear User,</p>
    <p>Your OTP is <b>{otp_code}</b>. This code is valid for 10 minutes.</p>
    <p><img src="cid:verification_image"></p>
    <p>Best regards,<br>[Your Company Name]</p>
  </body>
</html>
"""

        encoded_image = self._encode_image("/app/login/mail/web_otp.jpg")
        image_cid = 'verification_image'  # CID used in the HTML body

    # Construct the email with both plain text and HTML parts
        self.message = f"""From: {self.sender}
To: {self.receiver}
Subject: {self.subject}
MIME-Version: 1.0
Content-Type: multipart/related; boundary="sep"

--sep
Content-Type: text/plain; charset="UTF-8"
Content-Transfer-Encoding: 7bit

{body_text}

--sep
Content-Type: text/html; charset="UTF-8"
Content-Transfer-Encoding: 7bit

{body_html}

--sep
Content-Type: image/jpeg
Content-ID: <{image_cid}>
Content-Transfer-Encoding: base64

{encoded_image}

--sep--
"""

SERVER_ADDRESS='mail'
PORT=25

def send_email(sender: str, receiver: str, subject: str, body: str, otp_code: int):

    try:
        mail = Mail(
            sender=sender,
            receiver=receiver,
            subject=subject,
            body=body
        )
    except ValueError as err:
        logger.warning(f"Error: Missing Value(s) {err}")
        return None

    mail.build(otp_code)

    try:
        with smtplib.SMTP(SERVER_ADDRESS, PORT) as server:
            server.sendmail(sender, receiver, mail.message)
        return True

    except Exception as err:
        logger.error(f"Error: Unhandled {err}")
    return False

# Create your tests here.
class CrudTest(TestCase):

    username = "dummy"
    email = "dummy@gmail.es"
    password = make_password("dummy")
    otp_code = 1234
    sender_email = 'sender@example.com'  # Replace with your email address
    receiver_email = 'jvcaavzulgbqgzasbj@cazlq.com'  # Replace with the recipient's address
    subject = 'Test Email'
    body = 'This is a test email.'

    def test_send_email(self):


        print(f"opt_code: {self.otp_code}")
        self.assertEqual(send_email(self.sender_email, self.receiver_email, self.subject, self.body, self.otp_code), True)
        return
        self.assertEqual(send_email(self.sender_email, None, self.subject, self.body, self.otp_code), False)
        self.assertEqual(send_email(self.sender_email, self.receiver_email, None, self.body, self.otp_code), False)
        self.assertEqual(send_email(self.sender_email, self.receiver_email, self.subject, None, self.otp_code), False)
        self.assertEqual(send_email(self.sender_email, self.receiver_email, self.subject, self.body, None), False)


    def test_get_user_by_email(self):

        return

        models.user_login.objects.create(
            username=self.username,
            email=self.email,
            password=self.password
        )

        print("GET USER BY EMAIL TEST")
        self.assertEqual(get_user_by_email(None), None)
        self.assertEqual(get_user_by_email("test"), None)
        self.assertEqual(type(get_user_by_email(self.email)), models.user_login)
