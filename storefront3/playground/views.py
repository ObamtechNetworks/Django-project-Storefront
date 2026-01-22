from django.shortcuts import render
from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from templated_mail.mail import BaseEmailMessage # this class extends Django's EmailMessage
from .tasks import notify_customers

def say_hello(request):
    # try:
    #     # send_mail('subject', 'message', 'webmaster@localhost', ['user@example.com'])
    #     # mail_admins('subject', 'Here is the message.', html_message='<b>This is bold</b>')
    #     # message = EmailMessage(
    #     #     'Subject here',
    #     #     'Body goes here',
    #     #     'webmaster@localhost',
    #     #     ['user@example.com']
    #     # )
        
    #     # message.attach_file('playground/static/images/dog.png')
    #     # message.send()
    #     message = BaseEmailMessage(
    #         template_name='emails/hello.html', # specify the email template file to be used
    #         context={'name': 'Bamidele Michael'} # dynamic context data for rendering the template
    #     )
    #     message.send(to=['obams@example.com'])
    # except BadHeaderError:
    #     pass
    
    # ===> CELERY SECTION HERE
    notify_customers.delay("This is important notification for all our customers!")
    
    return render(request, 'hello.html', {'name': 'Bamidele'})
