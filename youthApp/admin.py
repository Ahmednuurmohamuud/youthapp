from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Admin, CompanyProfile, JobPosting, TrainingCourse, CustomUser, JobApplication, Lesson, Enrollment, Message, Portfolio, NetworkConnection, Notification, Education

admin.site.register(Admin)
admin.site.register(CompanyProfile)
admin.site.register(JobPosting)
admin.site.register(TrainingCourse)
admin.site.register(JobApplication)
admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(Message)
admin.site.register(Portfolio)
admin.site.register(NetworkConnection)
admin.site.register(Notification)
admin.site.register(Education)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'fullname', 'phone_number', 'user_type', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('fullname', 'phone_number', 'skills', 'education', 'cv_file', 'user_type')}),
    )


