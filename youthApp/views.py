from django.shortcuts import render, redirect, get_object_or_404
from .models import JobPosting,JobApplication
from .forms import JobForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.urls import reverse_lazy

from .models import TrainingCourse, Enrollment

from .forms import CourseForm
from .forms import RegistrationForm,JobApplicationForm



from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import CustomUser

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login_view')  # ha ku darin login(request, user)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()
    return render(request, 'user/Login_Registration/registration.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in!")
        return redirect('user_page')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('user_page')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'user/Login_Registration/login.html', {'form': form})




# def edit_profile(request):
#     profile, created = UserPro.objects.get_or_create(user=request.user)
#     if request.method == 'POST':
#         form = UserProForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('user_page')  # ama meeshii aad rabto
#     else:
#         form = UserProForm(instance=profile)
#     return render(request, 'user_profile/edit_profile.html', {'form': form})


def base_page(request):
    return render(request, 'admin/home.html')  # Make sure 'base.html' exists in the correct templates folder



@login_required(login_url=reverse_lazy('login_view'))
def apply_job(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            # Prevent duplicate applications
            if JobApplication.objects.filter(user=request.user, job=job).exists():
                messages.info(request, "You have already applied for this job.")
            else:
                application = form.save(commit=False)
                application.user = request.user
                application.job = job
                application.save()
                messages.success(request, "You have successfully applied for the job!")
                return redirect('user_page')  # Make sure 'index' is a valid view name
        else:
            messages.error(request, "There was an error with your application. Please check the form.")
    else:
        form = JobApplicationForm()

    return render(request, 'user/jobs/apply_job.html', {'form': form, 'job': job})

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
    user_pro = None
    if request.user.is_authenticated:
        user_pro = request.user  # if request.user is instance of CustomUser

    courses = TrainingCourse.objects.all()
    jobs = JobPosting.objects.all()

    return render(request, 'user/home.html', {
        'user_pro': user_pro,
        'courses': courses,
        'jobs': jobs
    })


@login_required
def user_dashboard(request):
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
    context = {
        'enrollments': enrollments,
    }
    return render(request, 'user/Course_page/dashboard.html', context)


def course_page(request):
    courses = TrainingCourse.objects.all()

    # Filter by category
    category = request.GET.get('category')
    if category:
        courses = courses.filter(category=category)

    # Filter by level
    level = request.GET.get('level')
    if level:
        courses = courses.filter(level=level)

    # Filter by max price
    price = request.GET.get('price')
    if price:
        try:
            price_val = float(price)
            courses = courses.filter(price__lte=price_val)
        except ValueError:
            pass

    # Filter by rating
    rating = request.GET.get('rating')
    if rating:
        try:
            rating_val = float(rating)
            courses = courses.filter(rating__gte=rating_val)
        except ValueError:
            pass

    # Filter by duration
    duration = request.GET.get('duration')
    if duration == 'short':
        courses = courses.filter(duration__lte=2)
    elif duration == 'medium':
        courses = courses.filter(duration__gt=2, duration__lte=6)
    elif duration == 'long':
        courses = courses.filter(duration__gt=6)

    context = {
        'courses': courses,
        # Pass current filters to template to keep selection after reload
        'selected_category': category or '',
        'selected_level': level or '',
        'selected_price': price or '100',
        'selected_rating': rating or '',
        'selected_duration': duration or '',
    }

    return render(request, 'user/Course_page/course.html', context)






# @login_required(login_url=reverse_lazy('login_view'))
def enrolled_courses(request, course_id):
    course = get_object_or_404(TrainingCourse, id=course_id)

    # Haddii aad rabto inaad hubiso in user-ku ku qoran yahay course-kaas:
    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()

    context = {
        'course': course,
        'enrollment': enrollment,
    }
    return render(request, 'user/Course_page/enrolled_courses.html', context)



@login_required
def course_detail(request, course_id):
    course = get_object_or_404(TrainingCourse, id=course_id)
    lessons = course.lessons.all()  # thanks to related_name='lessons'

    context = {
        'course': course,
        'lessons': lessons,
    }
    return render(request, 'user/Course_page/course_detail.html', context)






def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login_view')
