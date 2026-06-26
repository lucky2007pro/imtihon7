import threading
from django.core.mail import EmailMessage
from django.conf import settings

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def send_to_email(email, code):
    html_content = f"Tizimga kirish uchun tasdiqlash kodingiz: <b>{code}</b>"
    msg = EmailMessage(
        "Kutubxona Tizimi Tasdiqlash Kodi",
        html_content,
        settings.DEFAULT_FROM_EMAIL,
        [email]
    )
    msg.content_subtype = "html"
    EmailThread(msg).start()
