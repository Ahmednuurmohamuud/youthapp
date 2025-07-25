from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
User = settings.AUTH_USER_MODEL
import os
# from django.contrib.auth import get_user_model

# User = get_user_model()


class JobApplication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey('JobPosting' , on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)  # Field for resume
    cover_letter = models.FileField(upload_to='cover_letters/', null=True, blank=True)  # Field for cover letter
    additional_questions = models.TextField(null=True, blank=True)  # Field for additional questions

    class Meta:
        unique_together = ('user', 'job') 



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
    company_email = models.EmailField(max_length=255, null=True, blank=True)
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
    image = models.ImageField(upload_to='courses/images/', blank=True, null=True)
    status = models.CharField(max_length=50, choices=[
        ('upcoming', 'Upcoming'),
        ('active', 'Active'),
        ('completed', 'Completed')
    ], default='upcoming')
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, blank=True, null=True)
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES, blank=True, null=True)
    rating = models.FloatField(default=0)
    duration = models.IntegerField(default=0)

    def __str__(self):
        return self.course_name
    

    
class Enrollment(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(TrainingCourse, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.user.username} - {self.course.course_name}"



    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(TrainingCourse, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    

    
class Lesson(models.Model):
    course = models.ForeignKey(TrainingCourse, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)  # sax: max_length waa lama huraan
    lesson_type = models.CharField(
        max_length=10,  # sax: max_length=10 ayaa ku filan 'video' & 'text'
        choices=[('video', 'Video'), ('text', 'Text')]
    )
    video_url = models.URLField(blank=True, null=True)
    text_content = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.order}. {self.title}"




class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    skills = models.TextField(blank=True)
    education = models.TextField(blank=True)
    cv_file = models.FileField(upload_to='cv_uploads/', blank=True, null=True)
    user_type = models.CharField(choices=[('individual', 'Individual'), ('company', 'Company')], max_length=50)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  # ✅ cusub
  

    def __str__(self):
          return self.username
    

class NetworkConnection(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')

        
class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to='chat_uploads/', blank=True, null=True)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    is_image = models.BooleanField(default=False)
    is_audio = models.BooleanField(default=False)
    is_video = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Auto detect file type
        if self.file:
            ext = os.path.splitext(self.file.name)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.gif']:
                self.is_image = True
            elif ext in ['.mp3', '.wav', '.webm']:
                self.is_audio = True
            elif ext in ['.mp4', '.mov', '.avi']:
                self.is_video = True
        super().save(*args, **kwargs)



class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    education = models.TextField(blank=True)
    website = models.URLField(blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)


class Education(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='educations')
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=100)
    year = models.CharField(max_length=20)

