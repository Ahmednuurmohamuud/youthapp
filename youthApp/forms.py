from django import forms
from .models import JobPosting,CompanyProfile,TrainingCourse,UserPro
from django.core.exceptions import ValidationError

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
        }




class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserPro
        fields = ['username', 'fullname', 'email', 'phone_number', 'skills', 'education', 'cv_file', 'user_type', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        # Halkan waxaad ku dari kartaa shuruudo dheeraad ah haddii loo baahdo
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        return password

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['name', 'description', 'location']