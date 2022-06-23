from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_welcome_email(name,password, receiver):
    #creating message subject and subject
    subject = 'Welcome email'
    sender='apollolibrary99@gmail.com'

    #passing in the context variables
    text_context=render_to_string('email/newsemail.txt',{"name" :name, "password":password})
    html_context=render_to_string('email/newsemail.html',{"name" :name,"password":password})

    msg=EmailMultiAlternatives(subject,text_context,sender,[receiver])
    msg.attach_alternative(html_context,'text/html')
    msg.send()