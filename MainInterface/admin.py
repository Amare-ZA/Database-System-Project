from django.contrib import admin
from .models import (
    Message, Student, Module, Enrollment, Assignment, AssignmentSubmission,
    Announcement, StudyMaterial, Attendance, Grade, CourseEvaluation
)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_number', 'phone_number')
    search_fields = ('user__username', 'user__email', 'student_number')

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'lecturer', 'credits')
    search_fields = ('code', 'name', 'lecturer')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'module', 'enrollment_date')
    list_filter = ('module', 'enrollment_date')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('module', 'title', 'due_date', 'max_marks')
    list_filter = ('module', 'due_date')

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submission_date', 'marks')
    list_filter = ('assignment', 'submission_date')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'module')
    list_filter = ('module', 'date_posted')

@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('module', 'title', 'upload_date')
    list_filter = ('module', 'upload_date')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'module', 'date', 'is_present')
    list_filter = ('module', 'date', 'is_present')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'module', 'grade', 'grade_type')
    list_filter = ('module', 'grade_type')

@admin.register(CourseEvaluation)
class CourseEvaluationAdmin(admin.ModelAdmin):
    list_display = ('student', 'module', 'rating', 'submission_date')
    list_filter = ('module', 'rating')

admin.site.register(Message)
