from django.shortcuts import render
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from templated_mail.mail import BaseEmailMessage # this class extends Django's EmailMessage
from .tasks import notify_customers
from rest_framework.views import APIView
import requests

class HelloView(APIView):
    @method_decorator(cache_page(60*5))  # Cache the view for 5 minutes, this is how to decorate class-based views
    def get(self, request):
        # SIMULATING A SLOW API with caching eliminating the low-level cache implementation
        response = requests.get('https://httpbin.org/delay/2')  # Simulates a 2-second delay
        data = response.json()
        return render(request, 'hello.html', {'name': 'Bamidele'})

"""
@cache_page(60*5)  # Cache the view for 5 minutes, this works for a function-based view
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
    # notify_customers.delay("This is important notification for all our customers!")
    
    # return render(request, 'hello.html', {'name': 'Bamidele'})
    
    # SIMULATING A SLOW API with caching eliminating the low-level cache implementation
    response = requests.get('https://httpbin.org/delay/2')  # Simulates a 2-second delay
    data = response.json()
    return render(request, 'hello.html', {'name': data})
"""