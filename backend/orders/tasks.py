from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_id):
    """
    A task that sends a notification via email after 
    the successful creation of an order object.

    Parameters:
    - order_id (int): The ID of the newly created order.
    """
    order = Order.objects.get(id=order_id)
    subject = 'Zamówienie nr {}'.format(order.id)
    message = 'Hello, {}You have placed an order in our store.\
    The order ID is {}.'.format(order.name,
                                order.id)
    mail_sent = send_mail(subject,
                          message,
                          'admin@myshop.com',
                          [order.email])
    return mail_sent
