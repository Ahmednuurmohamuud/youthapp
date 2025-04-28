from django.shortcuts import render, redirect, get_object_or_404
from .models import JobPosting
from .forms import JobForm

from .models import TrainingCourse
from .forms import CourseForm

from .models import UserPro
from .forms import UserProForm



from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib import messages


def base_page(request):
    return render(request, 'admin/home.html')  # Make sure 'base.html' exists in the correct templates folder


def job_list(request):
    jobs = JobPosting.objects.all()
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'admin/Job_Registration/job_list.html', {'jobs': jobs, 'form': form, 'edit_mode': False})



#  mala isticmaaloyo function kaan
def job_create(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'admin/Job_Registration/jobReg_form.html', {'form': form})




def job_update(request, id):
    job = get_object_or_404(JobPosting, id=id)
    jobs = JobPosting.objects.all()
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_list')
    else:
        form = JobForm(instance=job)
    
    # Pass the 'edit_mode' flag and job instance to the template
    return render(request, 'admin/Job_Registration/job_list.html', {'form': form, 'edit_mode': True, 'job': job, 'jobs': jobs})



def job_delete(request, id):
    job = get_object_or_404(JobPosting, id=id)
    if request.method == "POST":
        job.delete()
        return redirect('job_list')
    return render(request, 'admin/Job_Registration/job_list.html', {'job': job})

# _____________________________TrainingCourse____________________________________________________________#


def course_list(request):
    courses = TrainingCourse.objects.all()
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'admin/Course_Registration/course_list.html', {'form': form, 'edit_mode': False, 'courses': courses })

#  mala isticmaaloyo function kaan
def course_create(request):
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'admin/Course_Registration/courseReg_form.html', {'form': form})





def course_update(request, id):
    course = get_object_or_404(TrainingCourse, id=id)
    courses = TrainingCourse.objects.all()
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'admin/Course_Registration/course_list.html', {'form': form, 'edit_mode': True, 'course': course, 'courses': courses })



def course_delete(request, id):
    course = get_object_or_404(TrainingCourse, id=id)
    if request.method == "POST":
        course.delete()
        return redirect('course_list')
    return render(request, 'admin/Course_Registration/course_list.html', {'course': course})


def user_page(request):
    jobs = JobPosting.objects.all()
    courses = TrainingCourse.objects.all()
    return render(request, 'user/home.html', {'jobs': jobs, 'courses': courses})


def course_page(request):

    jobs = JobPosting.objects.all()
    courses = TrainingCourse.objects.all()
    return render(request, 'user/Course_page/course.html', {'jobs': jobs, 'courses': courses})



def login(request):

    jobs = JobPosting.objects.all()
    courses = TrainingCourse.objects.all()
    return render(request, 'user/Login_Registration/login.html', {'jobs': jobs, 'courses': courses})







def registration(request):
    # Render the registration page
    form = UserProForm()  # Initialize an empty form
    return render(request, 'user/Login_Registration/registration.html', {'form': form})


def register_user(request):
    if request.method == "POST":
        form = UserProForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('user_page')  # Redirect to the user page after successful registration
    else:
        form = UserProForm()  # Initialize an empty form

    # Render the registration page with the form
    return render(request, 'user/Login_Registration/registration.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_page')  # Redirect to dashboard or homepage
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    
    return render(request, 'user/Login_Registration/login.html', {'form': form})