from django.shortcuts import render
from django.core.mail import send_mail, mail_admins, BadHeaderError


def say_hello(request):
    try:
        # send_mail('subject', 'message', 'webmaster@localhost', ['user@example.com'])
        mail_admins('subject', 'Here is the message.', html_message='<b>This is bold</b>')
    except BadHeaderError:
        pass
    return render(request, 'hello.html', {'name': 'Mosh'})
