"""Imports"""
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .forms import ContactForm


def contact(request):
    """A view to render the contact page"""

    if request.method == 'POST':

        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message was submitted successfully. \
                We will be in touch soon')
            return redirect(reverse('home'))

            instance = form.save()

            sender_email = instance.email
            subject = render_to_string(
                'contact/confirmation_emails/subject_contact_email.txt',
                {'instance': instance})
            body = render_to_string(
                'contact/confirmation_emails/body_contact_email.txt',
                {'instance': instance,
                 'contact_email': settings.DEFAULT_FROM_EMAIL})
            send_mail(
                subject,
                body, settings.DEFAULT_FROM_EMAIL,
                [sender_email]
            )
        else:
            messages.error(
                request, 'There was a problem with the form. \
                Please try again')

    form = ContactForm()

    template = 'contact/contact.html'
    context = {
        'form': form,
        'on_contact_page': True
    }

    return render(request, template, context)
