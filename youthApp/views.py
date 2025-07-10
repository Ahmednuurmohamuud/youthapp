from django.shortcuts import render, redirect, get_object_or_404
from .models import JobPosting,JobApplication
from .forms import JobForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .forms import MessageForm
from django.db.models import Q
from django.http import HttpResponseForbidden,JsonResponse



# from .models import TrainingCourse, Enrollment,Lesson

from .forms import CourseForm
from .forms import RegistrationForm,JobApplicationForm,ProfileForm,PortfolioForm,NetworkConnection,Portfolio,Notification,Education



from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import CustomUser

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets

from .models import (
    CustomUser, JobApplication, Admin, CompanyProfile,
    JobPosting, TrainingCourse, Enrollment, Lesson,NetworkConnection,Message
)
from .serializers import (
    CustomUserSerializer, JobApplicationSerializer, AdminSerializer,
    CompanyProfileSerializer, JobPostingSerializer, TrainingCourseSerializer,
    EnrollmentSerializer, LessonSerializer , NetworkConnectionSerializer
)

# REST API ViewSets
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

class CompanyProfileViewSet(viewsets.ModelViewSet):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer

class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    authentication_classes = [TokenAuthentication]  # ama JWTAuthentication
    permission_classes = [IsAuthenticated]  # kaliya users logged in allowed

class TrainingCourseViewSet(viewsets.ModelViewSet):
    queryset = TrainingCourse.objects.all()
    serializer_class = TrainingCourseSerializer
    authentication_classes = [TokenAuthentication]  # ama JWTAuthentication
    permission_classes = [IsAuthenticated]  # kaliya users logged in allowed

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class NetworkConnectionViewSet(viewsets.ModelViewSet):
    queryset = NetworkConnection.objects.all()
    serializer_class = NetworkConnectionSerializer




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




@login_required
def user_profile(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('user_profile')
        else:
            messages.error(request, "Please correct the errors below.")
            print(form.errors)
    else:
        form = ProfileForm(instance=user)

    return render(request, 'user/profile.html', {'form': form})


def base_page(request):
    return render(request, 'admin/home.html')  # Make sure 'base.html' exists in the correct templates folder

def home_page(request):
    return render(request, 'user/home.html') 


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


# def all_courses(request):
#     courses = TrainingCourse.objects.all()
#     return render(request, 'user/Course_page/all_courses.html', {'courses': courses})


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


def job_page(request):
    jobs = JobPosting.objects.all()

    location = request.GET.get('location')
    max_salary = request.GET.get('salary')

    if location:
        jobs = jobs.filter(location__icontains=location)


    if max_salary:
        try:
            jobs = jobs.filter(salary__lte=int(max_salary))
        except ValueError:
            pass



    context = {
        'jobs': jobs,
        
    }
    
    return render(request, 'user/jobs/job.html', context)







@login_required(login_url=reverse_lazy('login_view'))
def my_enrollments(request):
    # Diiwaangelinta user-ka
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')

    return render(request, 'user/course_page/my_enrollments.html', {
        'enrollments': enrollments
    })

@login_required(login_url=reverse_lazy('login_view'))
def course_lessons(request, course_id):
    course = get_object_or_404(TrainingCourse, id=course_id)
    lessons = course.lessons.order_by('order')

    # Hubi in user-ka enrolled yahay
    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        return redirect('user_page')

    return render(request, 'user/course_page/course_lessons.html', {
        'course': course,
        'lessons': lessons,
    })





@login_required(login_url=reverse_lazy('login_view'))
def network_page(request):
    users = CustomUser.objects.exclude(id=request.user.id)

    # Soo qaado connections-ka dhamaantood ee user-ka
    connections = NetworkConnection.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    )

    # Diyaari dict si sahlan loo baadho xaaladaha user kasta
    connection_dict = {}
    for conn in connections:
        if conn.sender == request.user:
            connection_dict[conn.receiver.id] = conn.status
        elif conn.receiver == request.user:
            connection_dict[conn.sender.id] = conn.status

    unread_count = request.user.notifications.filter(is_read=False).count()

    return render(request, 'user/networks_page/network.html', {
        'users': users,
        'connection_dict': connection_dict,
        'unread_count': unread_count,
    })



@login_required
def send_connection_request(request, user_id):
    to_user = get_object_or_404(CustomUser, id=user_id)
    connection, created = NetworkConnection.objects.get_or_create(sender=request.user, receiver=to_user, status='pending')
    if created:
        Notification.objects.create(user=to_user, message=f"{request.user.fullname} sent you a connection request")
    return redirect('network_page')


@login_required
def pending_requests(request):
    requests = NetworkConnection.objects.filter(receiver=request.user, status='pending')

    if request.method == 'POST':
        connection_id = request.POST.get('connection_id')
        action = request.POST.get('action')  # 'accept' or 'reject'
        
        try:
            connection = NetworkConnection.objects.get(id=connection_id, receiver=request.user, status='pending')
            if action == 'accept':
                connection.status = 'accepted'
                connection.save()
                messages.success(request, f"You have accepted connection request from {connection.sender.fullname}.")
            elif action == 'reject':
                connection.delete()
                messages.info(request, f"You have rejected connection request from {connection.sender.fullname}.")
        except NetworkConnection.DoesNotExist:
            messages.error(request, "Connection request not found or already processed.")
        
        return redirect('pending_requests')

    return render(request, 'user/networks_page/pendingrequests.html', {'requests': requests})


@login_required
def accept_connection_request(request, connection_id):
    connection = get_object_or_404(NetworkConnection, id=connection_id)

    # Hubi in user-ka uu yahay receiver-ka codsiga
    if connection.receiver == request.user and connection.status == 'pending':
        connection.status = 'accepted'
        connection.save()

        # U dir notification sender-ka
        Notification.objects.create(
            user=connection.sender,
            message=f"{request.user.fullname} accepted your connection request."
        )

    return redirect('network_page')


@login_required
def reject_connection_request(request, conn_id):
    conn = get_object_or_404(NetworkConnection, id=conn_id, receiver=request.user)
    conn.delete()
    Notification.objects.create(user=conn.sender, message=f"{request.user.fullname} rejected your connection request")
    return redirect('pending_requests')

 


@login_required(login_url=reverse_lazy('login_view'))
def connect_user(request, user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)

    # Check in case connection already exists
    connection, created = NetworkConnection.objects.get_or_create(
        sender=request.user,
        receiver=target_user,
        defaults={'status': 'pending'}
    )

    if created:
        # Abuur notification user-ka la diro
        Notification.objects.create(
            user=target_user,
            message=f"{request.user.fullname} has sent you a connection request."
        )
        messages.success(request, "Connection request sent successfully.")
    else:
        messages.info(request, "You have already sent a connection request to this user.")

    return redirect('network_page')

@login_required
def disconnect_user(request, user_id):
    other_user = get_object_or_404(CustomUser, id=user_id)
    connection = NetworkConnection.objects.filter(
        (Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)),
        status='accepted'
    ).first()

    if connection:
        connection.delete()
    
    return redirect('network_page')

@login_required(login_url=reverse_lazy('login_view'))
def user_profile_view(request, user_id):
    profile_user = get_object_or_404(CustomUser, id=user_id)

    is_connected = NetworkConnection.objects.filter(
        Q(sender=request.user, receiver=profile_user) | Q(sender=profile_user, receiver=request.user),
        status='accepted'
    ).exists()

    connection_status = None
    connection_id = None
    if not is_connected:
        pending_connection = NetworkConnection.objects.filter(
            Q(sender=request.user, receiver=profile_user) | Q(sender=profile_user, receiver=request.user)
        ).first()
        if pending_connection:
            connection_status = pending_connection.status
            connection_id = pending_connection.id

    portfolio = Portfolio.objects.filter(user=profile_user).first()

    return render(request, 'user/networks_page/profile.html', {
        'profile_user': profile_user,
        'portfolio': portfolio,
        'is_connected': is_connected,
        'connection_status': connection_status,
        'connection_id': connection_id
    })



@login_required
def portfolio_api(request, user_id):
    profile_user = get_object_or_404(CustomUser, id=user_id)
    portfolio = Portfolio.objects.filter(user=profile_user).first()

    if portfolio:
        data = {
            'bio': portfolio.bio,
            'education': portfolio.education,
            'experience': portfolio.experience,
            'website': portfolio.website,
            'github': portfolio.github,
            'linkedin': portfolio.linkedin,
        }
    else:
        data = {'error': 'No portfolio found.'}

    return JsonResponse(data)

@login_required
def edit_portfolio(request):
    try:
        portfolio = Portfolio.objects.get(user=request.user)
    except Portfolio.DoesNotExist:
        portfolio = None

    if request.method == 'POST':
        form = PortfolioForm(request.POST, instance=portfolio)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('user_profile')  # ama halka aad rabto
    else:
        form = PortfolioForm(instance=portfolio)

    return render(request, 'user/networks_page/edit_portfolio.html', {'form': form})

@login_required
def message_thread(request, user_id):
    other_user = get_object_or_404(CustomUser, id=user_id)

    # ✅ Hubi in ay connected yihiin
    is_connected = NetworkConnection.objects.filter(
        Q(sender=request.user, receiver=other_user, status='accepted') |
        Q(sender=other_user, receiver=request.user, status='accepted')
    ).exists()

    if not is_connected:
        return HttpResponseForbidden("You must be connected to message this user.")

    # ✅ Messages
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')

    # ✅ Update unread messages as read
    messages.filter(receiver=request.user, is_read=False).update(is_read=True)

    # ✅ POST request
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = other_user
            msg.save()

            # Optional notification
            Notification.objects.create(
                user=other_user,
                message=f"New message from {request.user.fullname}"
            )

            return redirect('message_thread', user_id=other_user.id)
    else:
        form = MessageForm()

    return render(request, 'user/networks_page/message.html', {
        'form': form,
        'messages': messages,
        'other_user': other_user,
    })


@login_required
def notifications_list(request):
    notifications = request.user.notifications.order_by('-created_at')[:5]
    return render(request, 'user/networks_page/notifications.html', {'notifications': notifications})

@login_required
def mark_notification_read(request, notification_id):
    notification = request.user.notifications.filter(id=notification_id).first()
    if notification:
        notification.is_read = True
        notification.save()
    return redirect('notifications_list')

@login_required
def mark_all_notifications_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect('notifications_list')

@login_required
def notification_redirect(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()

    # Halkan waxaan ka qaadeynaa user-ka soo diray connection request-ka
    # Assuming notification message-ka waxaa ku jira connection request
    # Laakiin si sax ah, waxaa fiican in Notification model aad ku xirto ForeignKey Connection ama User
    # Waxaan tusaale ahaan u qaadaneynaa in Notification model uu leeyahay 'connection' ForeignKey

    if hasattr(notification, 'connection'):
        conn = notification.connection
        other_user = conn.sender if conn.receiver == request.user else conn.receiver
        return redirect('user_profile_view', user_id=other_user.id)

    # Haddii aan connection la socon, redirect to notifications list or homepage
    return redirect('notifications_list')







@login_required(login_url=reverse_lazy('login_view'))
def companies_page(request):
    companies = CompanyProfile.objects.all()
    return render(request, 'user/companies_page/companies.html', {'companies': companies})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login_view')
