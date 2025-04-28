from django import forms
from .models import JobPosting,CompanyProfile,TrainingCourse,UserPro

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





class UserProForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': '!rounded-button block w-full pl-10 py-2 border border-gray-300 focus:ring-custom focus:border-custom',
            'placeholder': 'Enter password'
        }),
        required=True  # Ensures this field is required
    )
    class Meta:
        model = UserPro
        fields = ['username', 'fullname', 'phone_number', 'email', 'education', 'skills', 'user_type', 'cv_file']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': '!rounded-button block w-full pl-10 py-2 border border-gray-300 focus:ring-custom focus:border-custom',
                'placeholder': 'Username'
            }),
            'fullname': forms.TextInput(attrs={
                'class': '!rounded-button block w-full pl-10 py-2 border border-gray-300 focus:ring-custom focus:border-custom',
                'placeholder': 'Full Name'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': '!rounded-button block w-full pl-10 py-2 border border-gray-300 focus:ring-custom focus:border-custom',
                'placeholder': 'Phone Number'
            }),
            'email': forms.EmailInput(attrs={
                'class': '!rounded-button block w-full pl-10 py-2 border border-gray-300 focus:ring-custom focus:border-custom',
                'placeholder': 'Email Address'
            }),
            'education': forms.TextInput(attrs={
                'class': '!rounded-button block w-full pl-10 py-2 border border-gray-300 focus:ring-custom focus:border-custom',
                'placeholder': 'Highest degree earned'
            }),
            'skills': forms.Textarea(attrs={
                'class': '!rounded-button block w-full pl-10 py-2 border border-gray-300 focus:ring-custom focus:border-custom',
                'rows': 2,
                'placeholder': 'Separate skills with commas'
            }),
            'user_type': forms.Select(attrs={
                'class': '!rounded-button block w-full py-2 border border-gray-300 focus:ring-custom focus:border-custom'
            }),
            'cv_file': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-600 border border-gray-300 focus:ring-custom focus:border-custom'
            }),
            
            
            
        }




class LoginForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': '!rounded-button block w-full pl-10 py-2 border border-gray-300 focus:ring-custom focus:border-custom',
            'placeholder': 'Enter password'
        }),
        required=True  # Ensures this field is required
    )
    class Meta:
        model = UserPro
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': '!rounded-button block w-full pl-10 py-2 border border-gray-300 focus:ring-custom focus:border-custom',
                'placeholder': 'Username'
            }),     
        }



class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['name', 'description', 'location']