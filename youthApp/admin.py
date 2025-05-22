from django.contrib import admin
from .models import Admin, CompanyProfile, JobPosting, TrainingCourse, UserPro, JobApplication,  Lesson, Enrollment

admin.site.register(Admin)
admin.site.register(CompanyProfile)
admin.site.register(JobPosting)
admin.site.register(TrainingCourse)
admin.site.register(UserPro)
admin.site.register(JobApplication)
admin.site.register(Lesson)
admin.site.register(Enrollment)
