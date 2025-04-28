from django.urls import path
from .views import (
    base_page,
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
    login,
    registration,
    register_user,
    login_view
)

urlpatterns = [
    path('', base_page, name='base_page'),  # Base page route
    path('admin/Job_Registration/', job_list, name='job_list'),  
    path('admin/Job_Registration/new/', job_create, name='job_create'),
    path('admin/Job_Registration/edit/<int:id>/', job_update, name='job_update'),
    path('admin/Job_Registration/delete/<int:id>/', job_delete, name='job_delete'),
    path('admin/Course_Registration/', course_list, name='course_list'),  
    path('admin/Course_Registration/new/', course_create, name='course_create'),
    path('admin/Course_Registration/edit/<int:id>/', course_update, name='course_update'),
    path('admin/Course_Registration/delete/<int:id>/', course_delete, name='course_delete'),
    path('user/', user_page, name='user_page'),  
    path('user/Course_page/', course_page, name='course_page'),  
    path('user/Login_Registration/', login, name='login'),  
    path('user/Login_Registration/registration/', registration, name='registration'),  # Updated the URL
    path('user/Login_Registration/register/', register_user, name='register_user'),  # Updated the URL
    path('login/', login_view, name='login_view'),  # Updated the URL
]
