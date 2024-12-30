from celery import shared_task
from django.core.mail import send_mail
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from django.core.cache import cache
from .models import Order
import os



client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
token_url = os.getenv('ACCESS_TOKEN_URL')

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


@shared_task
def refresh_access_token():
    """
    A task that refreshes the access token for the application.
    """
    # Create an OAuth2 client
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)

    try:
        token_data = oauth.fetch_token(token_url=token_url, client_id=client_id, client_secret=client_secret)
    except Exception as e:
        raise ValueError("Error while fetching the token: " + str(e))

    # Store the access token in the cache
    expires_in = token_data['expires_in']
    cache.set('access_token', token_data['access_token'], timeout=expires_in - 60)
