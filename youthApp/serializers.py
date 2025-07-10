from rest_framework import serializers
from .models import (
    CustomUser, JobApplication, Admin, CompanyProfile, JobPosting,
    TrainingCourse, Enrollment, Lesson , NetworkConnection
)

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

class CompanyProfileSerializer(serializers.ModelSerializer):
     logo = serializers.SerializerMethodField()

     class Meta:
        model = CompanyProfile
        fields = ['name', 'logo']

        def get_logo(self, obj):
                request = self.context.get('request')
                if obj.logo:
                    return request.build_absolute_uri(obj.logo.url)
                return None

class JobPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = '__all__'

class TrainingCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingCourse
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'



class NetworkConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkConnection
        fields = '__all__'