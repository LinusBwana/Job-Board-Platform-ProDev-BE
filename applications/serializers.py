from rest_framework import serializers
from .models import ApplyJob
from .models import ApplyJob

class ApplyJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyJob
        fields = '__all__'
        read_only_fields = ['id', 'applicant', 'status', 'reviewed_by', 'reviewed_at', 'applied_on', 'resume']

class ApplicantHistorySerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title')
    company_name = serializers.CharField(source='job.company.name')
    job_location = serializers.SerializerMethodField()

    class Meta:
        model = ApplyJob
        fields = ['id', 'job_title', 'company_name','job_location', 'status']
        read_only_fields = ['job_title', 'company_name']

    def get_job_location(self, obj):
        job = obj.job  # go through the application
        """Returns formatted location(s) using Location's __str__ method"""
        if obj.job and obj.job.location.exists():
            locations = [str(location) for location in obj.job.location.all()]
            return " | ".join(locations)  # Separate multiple locations with |
        return None
    
class EmployerApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    applicant_name = serializers.SerializerMethodField()
    applicant_email = serializers.CharField(source='applicant.email', read_only=True)
    job_location = serializers.SerializerMethodField()

    class Meta:
        model = ApplyJob
        fields = ['id', 'job', 'job_title', 'applicant_name', 'applicant_email',
                  'job_location', 'status', 'applied_on','experience_years',
                  'expected_salary', 'cover_letter', 'resume']
        read_only_fields = ['id', 'job', 'job_title', 'applicant_name', 'applicant_email',
                            'job_location','applied_on','experience_years',
                            'expected_salary', 'cover_letter', 'resume']
        
    def get_applicant_name(self, obj):
        return f"{obj.applicant.first_name} {obj.applicant.last_name}"

    def get_job_location(self, obj):
        if obj.job and obj.job.location.exists():
            locations = [str(location) for location in obj.job.location.all()]
            return " | ".join(locations)
        return None