from datetime import datetime
from flask_mail import Message
from flask import request, render_template, current_app
from agil import mail
from threading import Thread
import string


def addMonth():
    import datetime
    return datetime.datetime.strptime(currentDate(), "%Y-%m-%d") + datetime.timedelta(days=30)


def currentDateTime():
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def currentDate():
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d")


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    thr = Thread(target=send_async_email, args=[current_app._get_current_object(), msg])
    thr.start()


def send_details_login(user):
    send_email("Détails des tentatives de connexion", "noreply@demo.com", [user.emailUser], "", render_template("./email/login.html", log=login_details()))


def send_details_logout(user):
    send_email("Détails de déconnexion","noreply@demo.com", [user.emailUser], "", render_template("./email/logout.html", log=login_details()))


def send_reset_email(user):
    send_email('Réinitialiser le mot de passe', "noreply@demo.com", [user.emailUser], "", render_template("./email/reset.html", user=user))


def send_confirmation_email(user):
    send_email('Réinitialiser le mot de passe', "noreply@demo.com", [user.emailUser], "", render_template("./email/confirmation.html", user=user))


def login_details():
    x = {
        "Ip": request.remote_addr,
        "Date": currentDateTime(),
        "Description": request.user_agent.platform + " " + request.user_agent.string
    }
    return x


def days_between(d2):
    Test = False
    d1 = datetime.strptime(str(currentDate()), "%Y-%m-%d")
    d2 = datetime.strptime(str(d2), "%Y-%m-%d")
    if (d2 - d1).days > 0:
        Test = True
    return Test


def FormatString(x):
    x = " ".join(x.split())
    return string.capwords(x)
