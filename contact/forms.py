from django import forms
from .models import ContactMessage, Newsletter

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control bg-light border-0', 'placeholder': 'Your Name', 'style': 'height: 55px;'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-light border-0', 'placeholder': 'Your Email', 'style': 'height: 55px;'}),
            'subject': forms.TextInput(attrs={'class': 'form-control bg-light border-0', 'placeholder': 'Subject', 'style': 'height: 55px;'}),
            'message': forms.Textarea(attrs={'class': 'form-control bg-light border-0', 'rows': 5, 'placeholder': 'Message'}),
        }

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
        }
