from django.db import models
import uuid
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
import random, string

# Create your models here.
class Industry(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    name = models.CharField(max_length=100, blank=False)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(max_length=500, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Industry'
        verbose_name_plural = 'Industries'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            # Handle duplicate slugs
            while Industry.objects.filter(slug=slug).exists():
                random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
                slug = f"{base_slug}-{random_str}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Location(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    country = models.CharField(max_length=100, null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    region = models.CharField(max_length=100, null=False, blank=False)
    is_remote = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='created_locations',null=True, blank=True
        )

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
        ordering = ['country', 'city', 'region']
        indexes = [
            models.Index(fields=['country', 'city', 'region']),
            models.Index(fields=['is_remote']),
        ]

    def __str__(self):
        parts = [self.country, self.city]
        if self.region:
            parts.append(self.region)
        location_str = ", ".join(parts)
        if self.is_remote:
            location_str += " - Remote"
        return location_str


class Company(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    locations = models.ManyToManyField(Location, related_name='companies')
    description = models.TextField(max_length=500, blank=False, null=False)
    logo = models.ImageField(
        upload_to='company_logos/',
        blank=True, 
        null=True
        )
    website_url = models.URLField(blank=True, null=True)
    industry = models.ForeignKey(Industry, on_delete=models.PROTECT, related_name='companies')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
        related_name='created_companies', null=True, blank=True
        )

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_verified']),
            models.Index(fields=['website_url']),
            models.Index(fields=['industry']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            # Use name + first 30 chars of description
            base_slug = f"{self.name} {self.description[:30]}"
            slug = base_slug
            # Handle duplicate slugs
            while Company.objects.filter(slug=slug).exists():
                random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
                slug = f"{base_slug}-{random_str}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Job(models.Model):
    job_type_choices = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]
    experience_level_choices = [
        ('entry', 'Entry Level'),
        ('mid_level', 'Mid Level'),
        ('senior', 'Senior Level'),
        ('lead', 'Lead'),
        ('executive', 'Executive'),
    ]
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='jobs')
    location = models.ManyToManyField(Location, related_name='jobs')
    job_type = models.CharField(
        choices=job_type_choices,
        max_length=50,
        default='full_time', 
    )
    experience_level = models.CharField(
        choices=experience_level_choices,
        max_length=50,
        default='entry', 
    )
    description = models.TextField()
    requirements = models.TextField(help_text="Comma-separated skills")
    responsibilities = models.TextField(help_text="Comma-separated skills")
    skills_required = models.TextField(help_text="Comma-separated skills")
    salary_min = models.DecimalField(max_digits=10, decimal_places=2,
                                     blank=True, null=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2,
                                     blank=True, null=True)
    salary_currency = models.CharField(max_length=3, default='Ksh')
    is_salary_visible = models.BooleanField(default=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    application_deadline = models.DateField()
    posted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
        ordering = ['-posted_on']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['industry']),
            models.Index(fields=['job_type']),
            models.Index(fields=['experience_level']),
            models.Index(fields=['company']),
            models.Index(fields=['is_active']),
            models.Index(fields=['is_active', 'industry']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.title}-{self.company.name}")
            slug = base_slug
            # Handle duplicate slugs
            while Job.objects.filter(slug=slug).exists():
                random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
                slug = f"{base_slug}-{random_str}"
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        if self.application_deadline:
            from django.utils import timezone
            return timezone.now() > self.application_deadline
        return False
    
    @property
    def salary_range(self):
        """Return formatted salary range"""
        if self.salary_min and self.salary_max:
            return f"{self.salary_currency} {self.salary_min:,.2f} - {self.salary_max:,.2f}"
        elif self.salary_min:
            return f"{self.salary_currency} {self.salary_min:,.2f}+"
        return "Not specified"
    
    def get_skills_list(self):
        """Return skills as a list"""
        if self.skills_required:
            return [skill.strip() for skill in self.skills_required.split(',')]
        return []

    def __str__(self):
        return f"{self.company.name} - {self.title}. Deadline is on {self.application_deadline}"