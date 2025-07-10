from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    base_page,
    home_page,
    job_create,
    job_update,
    job_delete,
    job_list,
    course_list,
    course_create,
    course_update,
    course_delete,
    user_page,
    course_page,
    register_view,
    login_view,
    logout_view,
    job_page,
    apply_job,
    user_profile,
    my_enrollments,
    course_lessons,
    network_page,
    connect_user,
    user_profile_view,
    send_connection_request,
    accept_connection_request,
    # send_message,
    message_thread,
    pending_requests,
    notifications_list,
    mark_notification_read,
    mark_all_notifications_read,
    notification_redirect,
    connect_user,
    disconnect_user,
    edit_portfolio,
    portfolio_api,
    companies_page,
    
    
    
    # --- REST API ViewSets ---
    CustomUserViewSet,
    JobApplicationViewSet,
    AdminViewSet,
    CompanyProfileViewSet,
    JobPostingViewSet,
    TrainingCourseViewSet,
    EnrollmentViewSet,
    LessonViewSet,
    NetworkConnectionViewSet,
)

# REST API Router
router = DefaultRouter()
router.register(r'api/users', CustomUserViewSet)
router.register(r'api/job-applications', JobApplicationViewSet)
router.register(r'api/admins', AdminViewSet)
router.register(r'api/companies', CompanyProfileViewSet)
router.register(r'api/jobs', JobPostingViewSet)
router.register(r'api/courses', TrainingCourseViewSet)
router.register(r'api/enrollments', EnrollmentViewSet)
router.register(r'api/lessons', LessonViewSet)
router.register(r'api/network', NetworkConnectionViewSet)

urlpatterns = [
    # 🌐 Frontend Views - Admin
    path('', base_page, name='base_page'),
    path('admin/Job_Registration/', job_list, name='job_list'),
    path('admin/Job_Registration/new/', job_create, name='job_create'),
    path('admin/Job_Registration/edit/<int:id>/', job_update, name='job_update'),
    path('admin/Job_Registration/delete/<int:id>/', job_delete, name='job_delete'),
    path('admin/Course_Registration/', course_list, name='course_list'),
    path('admin/Course_Registration/new/', course_create, name='course_create'),
    path('admin/Course_Registration/edit/<int:id>/', course_update, name='course_update'),
    path('admin/Course_Registration/delete/<int:id>/', course_delete, name='course_delete'),

    # 👤 User Views
    path('user/', user_page, name='user_page'),
    path('user/Course_page/', course_page, name='course_page'),
    path('user/Login_Registration/register/', register_view, name='register_view'),
    path('user/Login_Registration/login/', login_view, name='login_view'),
    path('user/logout/', logout_view, name='logout_view'),
    path('user/profile/', user_profile, name='user_profile'),
    path('user/jobs/job/', job_page, name='job_page'),
    path('apply/<int:job_id>/', apply_job, name='apply_job'),
    path('user/Course_page/my-enrollments/', my_enrollments, name='my_enrollments'),
    path('course/<int:course_id>/lessons/', course_lessons, name='course_lessons'),
    path('user/networks_page/network/', network_page, name='network_page'),
    path('network/connect/<int:user_id>/', connect_user, name='connect_user'),
    # urls.network
    path('network/connect/<int:user_id>/', send_connection_request, name='send_connection_request'),        
    path('network/message/<int:user_id>/', message_thread, name='message_thread'),
    path('user/networks_page/pending_requests/', pending_requests, name='pending_requests'),
    path('profile/<int:user_id>/', user_profile_view, name='user_profile_view'),
    path('connect/<int:user_id>/', connect_user, name='connect_user'),
    path('disconnect/<int:user_id>/',disconnect_user, name='disconnect_user'),

    path('accept-connection/<int:connection_id>/', accept_connection_request, name='accept_connection_request'),
    path('edit-portfolio/', edit_portfolio, name='edit_portfolio'),
    path('api/portfolio/<int:user_id>/',portfolio_api, name='portfolio_api'),
   
    path('notifications/', notifications_list, name='notifications_list'),
    path('notifications/mark-read/<int:notification_id>/', mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', mark_all_notifications_read, name='mark_all_notifications_read'),
    path('notification/<int:notification_id>/redirect/', notification_redirect, name='notification_redirect'),

    path('companies/', companies_page, name='companies_page'),

    # 🔌 REST API Endpoints
    path('', include(router.urls)),
]
