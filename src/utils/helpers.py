from django.core import mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string


def send_mail(subject, sender, receiver, template_name, context=None):
    # assert is
    mail_subject = 'Activate your Currentic Account.'
    message = render_to_string(template_name, context)
    plain_message = strip_tags(message)
    # from_email = 'CurrenticX Onboarding Team <onboarding@currenticx.com>'
    # to_email = user.email
    mail.send_mail(subject, plain_message, sender, receiver, html_message=message)
