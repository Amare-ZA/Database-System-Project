from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Message

def home(request):
    return render(request, 'MainInterface/home.html')

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect based on user type
            if user_type == 'student':
                return redirect('student_dashboard')
            elif user_type == 'lecturer':
                return redirect('lecturer_dashboard')
            elif user_type == 'administrator':
                return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'MainInterface/home.html')

def portal(request):
    return render(request, 'MainInterface/portal.html')


def message_list(request):
    messages = Message.objects.all().order_by('-created_at')
    return render(request, 'MainInterface/messages.html', {'messages': messages})

# Add these new views for different dashboards
def student_dashboard(request):
    return render(request, 'MainInterface/student_dashboard.html')

def lecturer_dashboard(request):
    return render(request, 'MainInterface/lecturer_dashboard.html')

def admin_dashboard(request):
    return render(request, 'MainInterface/admin_dashboard.html')