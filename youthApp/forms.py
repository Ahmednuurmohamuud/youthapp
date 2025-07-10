from django import forms
from django.conf import settings
from .models import JobPosting, CompanyProfile, TrainingCourse, CustomUser, JobApplication,NetworkConnection
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from .models import Message, Portfolio,Notification,Education




class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'user_type', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash password
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'profile_picture',
            'fullname',
            'email',
            'phone_number',
            'skills',
            'education',
            'cv_file',
            'user_type'
        ]
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3}),
            'education': forms.Textarea(attrs={'rows': 3}),
        }

class JobForm(forms.ModelForm):
    company = forms.ModelChoiceField(
        queryset=CompanyProfile.objects.all(),
        empty_label="Select Company",
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )

    class Meta:
        model = JobPosting
        fields = '__all__'
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'job_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'application_deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control select2'}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = TrainingCourse
        fields = '__all__'
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control'}),
            'course_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'instructor': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control select2'}),
            'category': forms.Select(choices=TrainingCourse.CATEGORY_CHOICES, attrs={'class': 'form-control'}),
            'level': forms.Select(choices=TrainingCourse.LEVEL_CHOICES, attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control', 
                'step': '0.1', 
                'min': 0, 
                'max': 5
            }),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),

        }




class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['name', 'description', 'location']



class JobApplicationForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True, label='Full Name')
    email = forms.EmailField(required=True, label='Email Address')
    
    class Meta:
        model = JobApplication
        fields = ['resume', 'cover_letter', 'additional_questions']

    resume = forms.FileField(required=True, label='Upload Your Resume')
    cover_letter = forms.FileField(required=False, label='Upload Your Cover Letter')
    additional_questions = forms.CharField(widget=forms.Textarea, required=False, label='Any Additional Information or Questions')

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'file']



class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['bio', 'experience', 'skills', 'education', 'website', 'github', 'linkedin']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'experience': forms.Textarea(attrs={'rows': 3}),
            'skills': forms.Textarea(attrs={'rows': 2}),
            'education': forms.Textarea(attrs={'rows': 2}),
        }

class NetworkConnection(forms.ModelForm):
    class Meta:
        model = NetworkConnection  # ← Ku beddel model sax ah
        fields = '__all__'     # ama ['field1', 'field2']