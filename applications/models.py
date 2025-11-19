from django.db import models
import uuid
from jobs.models import Job
from django.conf import settings

# save application documents in different directories for each user
def user_directory_path(instance, filename):
    # instance: the Application object
    # instance.applicant is the user
    return f'application_documents/user_{instance.applicant.id}/{filename}'

# Create your models here.
class ApplyJob(models.Model):
    status_choices = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interview'),
        ('rejected', 'Rejected'),
    ]
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='apply_job')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(
        choices=status_choices,
        max_length=50,
        default='pending',
    )
    cover_letter = models.TextField()
    resume = models.FileField(
        upload_to=user_directory_path,
        blank=False, 
        null=False,
    )
    additional_documents = models.FileField(
        upload_to=user_directory_path,
        blank=True, 
        null=True,
    )
    experience_years = models.PositiveIntegerField(default=0)
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, 
                                          blank=False, null=False)
    availability_date = models.DateField()
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.SET_NULL, 
                                    null=True, related_name='reviewed_applications')
    reviewed_at = models.DateTimeField(blank=True, null=True,
                                       help_text="Date and time when the application was reviewed")
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "Applications"
        ordering = ['-applied_on']
        indexes = [
            models.Index(fields=['job']),
            models.Index(fields=['applicant']),
            models.Index(fields=['status']),
            models.Index(fields=['applied_on']),
        ]

    def __str__(self):
        return f"{self.job.company.name} - {self.job.title} applied on {self.applied_on}. Stage: {self.status})"
    

class ApplicationHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, 
                          editable=False, unique=True)
    application = models.ForeignKey(ApplyJob,
                                    on_delete=models.CASCADE,
                                    related_name='status_history')
    status = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Application History"
        verbose_name_plural = "Application Histories"
        indexes = [
            models.Index(fields=['application']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.application.applicant} - {self.status} applied on {self.application.applied_on}"