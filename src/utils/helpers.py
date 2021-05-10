import string
import random
from datetime import timedelta

from django.core import mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.utils import timezone

from rest_framework_simplejwt.tokens import RefreshToken


def send_mail(subject, sender, receiver, template_name, context=None):
    """
    This helper function helps to send mails to list of users

    :param subject: subject of the email being sent
    :param sender: email sender
    :param receiver: email receiver
    :param template_name: path to template to be used for the emai;
    :param context: extra contents to be passed to the email content
    :return: None
    """
    message = render_to_string(template_name, context)
    plain_message = strip_tags(message)
    mail.send_mail(subject, plain_message, sender, receiver, html_message=message)


def token_generator(size=6, chars=string.ascii_uppercase + string.digits, seconds=None, expires_at=None):
    """
    Generates a random string by using a time object as the seed \n

    parameters:
        size (int): The number of string to be generated
        chars (Fixed): A random generated ascii and digits generated from the string module and concatenated together
        seconds (int): A specified number of seconds the token is expected to last for
        expires_at (datetime): A specified timestamp at which the token is expected to expire
    returns:
        token: the generated token
        expires_at: The specified or timestamp at which the token is expected to expire
    """
    if not expires_at:
        expires_at = timezone.now() + timedelta(seconds=seconds)
    random.seed(expires_at)
    return ''.join(random.choice(chars) for _ in range(size)), expires_at


def get_tokens_for_user(user):
    """
    This helper function helps to get the jwt token for a user
    :param user:
    :return:
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
