from time import sleep
# from storefront.celery import celery # with this approach our playground app is being dependent on storefront app, which is not best

# a better way is to go to the celery module and import a shared_task function
from celery import shared_task

@shared_task
def notify_customers(message):
    print("sending 10k emails..")
    print(message)
    sleep(10)
    print("Emails were successfully sent!")