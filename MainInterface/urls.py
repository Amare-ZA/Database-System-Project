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
    
    # Student Dashboard URLs
    path('student/profile/update/', views.update_profile, name='update_profile'),
    path('student/courses/', views.enrolled_courses, name='enrolled_courses'),
    path('student/courses/enroll/', views.enroll_course, name='enroll_course'),
    path('student/timetable/', views.view_timetable, name='view_timetable'),
    path('student/announcements/', views.view_announcements, name='view_announcements'),
    path('student/calendar/', views.academic_calendar, name='academic_calendar'),
    path('student/grades/', views.view_grades, name='view_grades'),
    path('student/attendance/', views.view_attendance, name='view_attendance'),
    path('student/materials/', views.study_materials, name='study_materials'),
    path('student/materials/download/<int:material_id>/', views.download_material, name='download_material'),
    path('student/assignments/', views.view_assignments, name='view_assignments'),
    path('student/assignments/submit/<int:assignment_id>/', views.submit_assignment, name='submit_assignment'),
    path('student/assignments/feedback/<int:assignment_id>/', views.assignment_feedback, name='assignment_feedback'),
    path('student/quizzes/', views.available_quizzes, name='available_quizzes'),
    path('student/quizzes/take/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('student/past-papers/', views.past_papers, name='past_papers'),
    path('student/progress/', views.academic_progress, name='academic_progress'),
    path('student/evaluation/<int:module_id>/', views.course_evaluation, name='course_evaluation'),
]