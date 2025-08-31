from django.shortcuts import render
from django.template.exceptions import TemplateDoesNotExist
from django.http import HttpResponse
from .models import Message

def home(request):
    return render(request, 'MainInterface/home.html')

def portal(request):
    return render(request, 'MainInterface/portal.html')


def message_list(request):
    messages = Message.objects.all().order_by('-created_at')
    return render(request, 'MainInterface/messages.html', {'messages': messages})