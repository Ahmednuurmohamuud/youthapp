from django.shortcuts import render, redirect, get_object_or_404
from .models import JobPosting
from .forms import JobForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

from .models import TrainingCourse,JobApplication,CourseEnrollment
from .forms import CourseForm

from .models import UserPro
from .forms import RegistrationForm



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


# def user_page(request):
#     jobs = JobPosting.objects.all()
#     courses = TrainingCourse.objects.all()
#     return render(request, 'user/home.html', {'jobs': jobs, 'courses': courses})


def user_page(request):
    jobs = JobPosting.objects.all()
    courses = TrainingCourse.objects.all()

    # flag: haddii uu login-galay
    is_logged_in = request.user.is_authenticated

    return render(request, 'user/home.html', {
        'jobs': jobs,
        'courses': courses,
        'is_logged_in': is_logged_in
    })


def course_page(request):

    jobs = JobPosting.objects.all()
    courses = TrainingCourse.objects.all()
    return render(request, 'user/Course_page/course.html', {'jobs': jobs, 'courses': courses})




# def login(request):

#     jobs = JobPosting.objects.all()
#     courses = TrainingCourse.objects.all()
#     return render(request, 'user/Login_Registration/login.html', {'jobs': jobs, 'courses': courses})


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id)

    # Check if user has already applied
    application, created = JobApplication.objects.get_or_create(user=request.user, job=job)
    if created:
        messages.success(request, "You have successfully applied for this job.")
    else:
        messages.info(request, "You have already applied for this job.")

    return redirect('user_page')

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(TrainingCourse, id=course_id)
    enrollment, created = CourseEnrollment.objects.get_or_create(user=request.user, course=course)
    if created:
        messages.success(request, "You have successfully enrolled in the course.")
    else:
        messages.info(request, "You are already enrolled in this course.")
    return redirect('user_page')






# def registration(request):
#     # Render the registration page
#     form = UserProForm()  # Initialize an empty form
#     return render(request, 'user/Login_Registration/registration.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Account created successfully. You can now login.")
            return redirect('login_view')  # Hubi in magacan sax yahay
    else:
        form = RegistrationForm()
    
    return render(request, 'user/Login_Registration/registration.html', {'form': form})


   

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = UserPro.objects.get(username=username)
                if check_password(password, user.password):  # Isticmaal check_password!
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    messages.success(request, "Login successful.")
                    return redirect('user_page')  # Badal hadii aad rabto page kale
                else:
                    messages.error(request, "Invalid password.")
            except UserPro.DoesNotExist:
                messages.error(request, "User does not exist.")
    else:
        form = LoginForm()

    return render(request, 'user/Login_Registration/login.html', {'form': form})

def logout_view(request):
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect('login')