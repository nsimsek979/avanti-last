from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactInfo, ContactMessage, Newsletter
from .forms import ContactMessageForm, NewsletterForm

def contact(request):
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            contact_message = form.save(commit=False)
            contact_message.ip_address = request.META.get('REMOTE_ADDR')
            contact_message.save()
            
            # Send email notification
            try:
                subject = f"New Contact Message: {contact_message.subject}"
                message = f"""
New contact message received:

Name: {contact_message.name}
Email: {contact_message.email}
Subject: {contact_message.subject}

Message:
{contact_message.message}

---
IP Address: {contact_message.ip_address}
Received at: {contact_message.created_at}
                """
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email sending failed: {e}")
            
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact:index')
    else:
        form = ContactMessageForm()
    
    context = {
        'contact_info': contact_info,
        'form': form,
    }
    return render(request, 'contact/contact.html', context)

def newsletter_subscribe(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'You have successfully subscribed to our newsletter!')
            except:
                messages.error(request, 'This email is already subscribed.')
        else:
            messages.error(request, 'Please enter a valid email address.')
    
    return redirect(request.META.get('HTTP_REFERER', '/'))
