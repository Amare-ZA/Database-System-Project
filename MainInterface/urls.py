from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.custom_login, name='login'),  # Add this line
    path('portal/', views.portal, name='portal'),
    path('messages/', views.message_list, name='message_list'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.custom_login, name='login'),
    path('portal/', views.portal, name='portal'),
    path('messages/', views.message_list, name='message_list'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('lecturer/', views.lecturer_dashboard, name='lecturer_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
]