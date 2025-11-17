from rest_framework import serializers
from .models import Application
from jobs.serializers import JobSerializer

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'job', 'cover_letter', 'resume', 'additional_documents', 'applicant', 
                  'experience_years', 'expected_salary', 'availability_date']
        read_only_fields = ['reviewed_by', 'reviewed_at', 'status', 'applied_on']

class ApplicantHistorySerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    company_name = serializers.CharField(source='job.company.name', read_only=True)
    job_location = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = ['id', 'job', 'job_title', 'company_name','job_location']

    def get_job_location(self, obj):
        """Returns formatted location(s) using Location's __str__ method"""
        if obj.job and obj.job.location.exists():
            locations = [str(location) for location in obj.job.location.all()]
            return " | ".join(locations)  # Separate multiple locations with |
        return None
    
class EmployerApplicationSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    applicant_name = serializers.SerializerMethodField()
    applicant_email = serializers.CharField(source='applicant.email', read_only=True)
    job_location = serializers.SerializerMethodField()

    class Meta:
        model = Application
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