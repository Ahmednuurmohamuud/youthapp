from django.contrib import admin
from .models import Admin, CompanyProfile, JobPosting, TrainingCourse, UserPro, JobApplication, CourseEnrollment

admin.site.register(Admin)
admin.site.register(CompanyProfile)
admin.site.register(JobPosting)
admin.site.register(TrainingCourse)
admin.site.register(UserPro)
admin.site.register(JobApplication)
admin.site.register(CourseEnrollment)
