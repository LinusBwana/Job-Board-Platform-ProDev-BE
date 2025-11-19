from django.contrib import admin
from .models import ApplyJob

class ApplyJobAdmin(admin.ModelAdmin):
    list_display = ['job', 'status']
admin.site.register(ApplyJob, ApplyJobAdmin)