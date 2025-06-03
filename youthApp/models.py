from django.db import models
from django.contrib.auth.models import User


class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey('JobPosting' , on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)  # Field for resume
    cover_letter = models.FileField(upload_to='cover_letters/', null=True, blank=True)  # Field for cover letter
    additional_questions = models.TextField(null=True, blank=True)  # Field for additional questions

    class Meta:
        unique_together = ('user', 'job') 

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('TrainingCourse', on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.course_name}"

# Create your models here.

class Admin(models.Model):
    username = models.CharField(max_length=20, unique=True, primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=[('superadmin', 'Super Admin'), ('admin', 'Admin')], default='admin')
    password = models.CharField(max_length=255)
    registration_date = models.DateField(auto_now_add=True)


class CompanyProfile(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)  # 👈 Logo field

    def __str__(self):
        return self.name  # Return the company name when the object is represented as a string






class JobPosting(models.Model):
    job_title = models.CharField(max_length=255)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    job_description = models.TextField()
    requirements = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    application_deadline = models.DateField()
    status = models.CharField(choices=[('approved', 'Approved'), ('pending', 'Pending'), ('rejected', 'Rejected')], max_length=50)



class TrainingCourse(models.Model):
    CATEGORY_CHOICES = [
    ('Development', 'Development'),
    ('Business', 'Business'),
    ('Design', 'Design'),
    ('Marketing', 'Marketing'),
]

    LEVEL_CHOICES = [
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced'),
]
    course_name = models.CharField(max_length=255)
    course_description = models.TextField()
    instructor = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='youthApp/static/images/', blank=True, null=True)  # Image field
    status = models.CharField(max_length=50, choices=[
        ('upcoming', 'Upcoming'),
        ('active', 'Active'),
        ('completed', 'Completed')
    ], default='upcoming')  # Status field with predefined choices
# Add these fields if you want to filter/sort by them:
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, blank=True, null=True)
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES, blank=True, null=True)
    rating = models.FloatField(default=0)  # e.g. 0 to 5 stars
    duration = models.IntegerField(default=0)  # number of hours
   



class Lesson(models.Model):
    LESSON_TYPE_CHOICES = [
        ('video', 'Video'),
        ('text', 'Text'),
    ]

    course = models.ForeignKey(TrainingCourse, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_url = models.URLField(blank=True, null=True)  # for video lessons (e.g. YouTube or uploaded link)
    text_content = models.TextField(blank=True, null=True)  # for text lessons
    lesson_type = models.CharField(max_length=10, choices=LESSON_TYPE_CHOICES)

    def __str__(self):
        return f"{self.course.course_name} - {self.title}"



class UserPro(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=255, unique=True)
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    skills = models.TextField()
    education = models.TextField()
    cv_file = models.FileField(upload_to='youthApp/static/cv_uploads/')
    user_type = models.CharField(choices=[('individual', 'Individual'), ('company', 'Company')], max_length=50)
    password = models.CharField(max_length=255)

    
