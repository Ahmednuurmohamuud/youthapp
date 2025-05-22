from django.shortcuts import render, redirect, get_object_or_404
from .models import JobPosting
from .forms import JobForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

from .models import TrainingCourse,JobApplication
from .forms import CourseForm

from .models import UserPro,Enrollment
from .forms import RegistrationForm,JobApplicationForm



from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib import messages



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




def apply_job(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            # Prevent user from applying twice for the same job
            if JobApplication.objects.filter(user=request.user, job=job).exists():
                messages.info(request, "You have already applied for this job.")
            else:
                application = form.save(commit=False)
                application.user = request.user
                application.job = job
                application.save()
                messages.success(request, "You have successfully applied for the job!")
                return redirect('user/user_page')  # Redirect to a job listings page or another relevant page
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
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    
    if not user_id:
        return redirect('login_view')
    
    # Halkan waxaad kusoo ururin kartaa jobs/courses user-ka
    courses = TrainingCourse.objects.all()
    jobs = JobPosting.objects.all()

    return render(request, 'user/home.html', {
        'username': username,
        'courses': courses,
        'jobs': jobs
    })
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






@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(TrainingCourse, id=course_id)
    already_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()

    if already_enrolled:
        messages.info(request, "You are already enrolled in this course.")
    else:
        Enrollment.objects.create(user=request.user, course=course)
        messages.success(request, "You have been successfully enrolled in this course.")

    return redirect('user/Course_page/course_detail.html', course_id=course.id)


@login_required
def course_detail(request, course_id):
    course = get_object_or_404(TrainingCourse, id=course_id)
    return render(request, 'user/Course_page/course_detail.html', {'course': course})



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
    return redirect('login_view')
