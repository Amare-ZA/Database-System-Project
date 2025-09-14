from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import (
    Message, Student, Module, Enrollment, Assignment, AssignmentSubmission,
    Announcement, StudyMaterial, Attendance, Grade, CourseEvaluation
)
from django.db.models import Avg
from datetime import datetime, timedelta

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

# Student Dashboard Views
@login_required
def student_dashboard(request):
    # Try to get the student profile or create one if it doesn't exist
    student, created = Student.objects.get_or_create(
        user=request.user,
        defaults={
            'student_number': f'STU{request.user.id:06d}',  # Generate a default student number
        }
    )
    
    # Get enrolled courses
    enrollments = Enrollment.objects.filter(student=student)
    enrolled_modules = [e.module for e in enrollments]
    
    # Get available modules (modules student isn't enrolled in yet)
    available_modules = Module.objects.exclude(id__in=[m.id for m in enrolled_modules])
    
    context = {
        'student': student,
        'enrolled_courses': enrollments,
        'announcements': Announcement.objects.all().order_by('-date_posted')[:5],
        'upcoming_assignments': Assignment.objects.filter(
            due_date__gte=datetime.now()
        ).order_by('due_date')[:5],
        'available_modules': available_modules
    }
    return render(request, 'MainInterface/student_dashboard.html', context)

@login_required
def update_profile(request):
    student = get_object_or_404(Student, user=request.user)
    if request.method == 'POST':
        student.phone_number = request.POST.get('phone')
        if 'profile_picture' in request.FILES:
            student.profile_picture = request.FILES['profile_picture']
        student.save()
        
        user = student.user
        user.first_name = request.POST.get('fullname').split()[0]
        user.last_name = ' '.join(request.POST.get('fullname').split()[1:])
        user.email = request.POST.get('email')
        user.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('student_dashboard')
    return render(request, 'MainInterface/update_profile.html', {'student': student})

@login_required
def enrolled_courses(request):
    student = get_object_or_404(Student, user=request.user)
    enrollments = Enrollment.objects.filter(student=student)
    return render(request, 'MainInterface/enrolled_courses.html', {'enrollments': enrollments})

@login_required
def enroll_course(request):
    if request.method == 'POST':
        student = get_object_or_404(Student, user=request.user)
        module_id = request.POST.get('module')
        
        if not module_id:
            messages.error(request, 'Please select a module to enroll in.')
            return redirect('student_dashboard')
            
        try:
            module = Module.objects.get(id=module_id)
            
            # Check if already enrolled
            if Enrollment.objects.filter(student=student, module=module).exists():
                messages.warning(request, f'You are already enrolled in {module.code}')
            else:
                # Create new enrollment
                Enrollment.objects.create(student=student, module=module)
                messages.success(request, f'Successfully enrolled in {module.code}')
                
        except Module.DoesNotExist:
            messages.error(request, 'Selected module not found.')
        except Exception as e:
            messages.error(request, f'Error during enrollment: {str(e)}')
            
    return redirect('student_dashboard')

@login_required
def view_timetable(request):
    student = get_object_or_404(Student, user=request.user)
    enrollments = Enrollment.objects.filter(student=student)
    return render(request, 'MainInterface/timetable.html', {'enrollments': enrollments})

@login_required
def view_announcements(request):
    announcements = Announcement.objects.all().order_by('-date_posted')
    return render(request, 'MainInterface/announcements.html', {'announcements': announcements})

@login_required
def academic_calendar(request):
    return render(request, 'MainInterface/academic_calendar.html')

@login_required
def view_grades(request):
    student = get_object_or_404(Student, user=request.user)
    grades = Grade.objects.filter(student=student)
    return render(request, 'MainInterface/grades.html', {'grades': grades})

@login_required
def view_attendance(request):
    student = get_object_or_404(Student, user=request.user)
    attendance = Attendance.objects.filter(student=student)
    return render(request, 'MainInterface/attendance.html', {'attendance': attendance})

@login_required
def study_materials(request):
    student = get_object_or_404(Student, user=request.user)
    enrollments = Enrollment.objects.filter(student=student)
    materials = StudyMaterial.objects.filter(module__in=[e.module for e in enrollments])
    return render(request, 'MainInterface/study_materials.html', {'materials': materials})

@login_required
def download_material(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)
    response = HttpResponse(material.file, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{material.file.name}"'
    return response

@login_required
def view_assignments(request):
    student = get_object_or_404(Student, user=request.user)
    enrollments = Enrollment.objects.filter(student=student)
    assignments = Assignment.objects.filter(module__in=[e.module for e in enrollments])
    return render(request, 'MainInterface/assignments.html', {'assignments': assignments})

@login_required
def submit_assignment(request, assignment_id):
    if request.method == 'POST':
        student = get_object_or_404(Student, user=request.user)
        assignment = get_object_or_404(Assignment, id=assignment_id)
        submission = AssignmentSubmission.objects.create(
            assignment=assignment,
            student=student,
            submission_file=request.FILES['assignment_file']
        )
        messages.success(request, 'Assignment submitted successfully!')
        return redirect('view_assignments')
    assignment = get_object_or_404(Assignment, id=assignment_id)
    return render(request, 'MainInterface/submit_assignment.html', {'assignment': assignment})

@login_required
def assignment_feedback(request, assignment_id):
    student = get_object_or_404(Student, user=request.user)
    submission = get_object_or_404(
        AssignmentSubmission,
        assignment_id=assignment_id,
        student=student
    )
    return render(request, 'MainInterface/assignment_feedback.html', {'submission': submission})

@login_required
def available_quizzes(request):
    student = get_object_or_404(Student, user=request.user)
    enrollments = Enrollment.objects.filter(student=student)
    # Add quiz functionality when implementing online quizzes
    return render(request, 'MainInterface/quizzes.html')

@login_required
def take_quiz(request, quiz_id):
    # Add quiz taking functionality when implementing online quizzes
    return render(request, 'MainInterface/take_quiz.html')

@login_required
def past_papers(request):
    student = get_object_or_404(Student, user=request.user)
    enrollments = Enrollment.objects.filter(student=student)
    return render(request, 'MainInterface/past_papers.html', {'enrollments': enrollments})

@login_required
def academic_progress(request):
    student = get_object_or_404(Student, user=request.user)
    grades = Grade.objects.filter(student=student)
    gpa = grades.aggregate(Avg('grade'))['grade__avg'] or 0
    return render(request, 'MainInterface/academic_progress.html', {
        'grades': grades,
        'gpa': gpa
    })

@login_required
def course_evaluation(request, module_id):
    if request.method == 'POST':
        student = get_object_or_404(Student, user=request.user)
        module = get_object_or_404(Module, id=module_id)
        CourseEvaluation.objects.create(
            student=student,
            module=module,
            rating=request.POST.get('rating'),
            comments=request.POST.get('comments')
        )
        messages.success(request, 'Evaluation submitted successfully!')
        return redirect('student_dashboard')
    module = get_object_or_404(Module, id=module_id)
    return render(request, 'MainInterface/course_evaluation.html', {'module': module})

def lecturer_dashboard(request):
    return render(request, 'MainInterface/lecturer_dashboard.html')

def admin_dashboard(request):
    return render(request, 'MainInterface/admin_dashboard.html')