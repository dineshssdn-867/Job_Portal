from django.db import models
from django_quill.fields import QuillField

from job_portal import settings
from django.template.defaultfilters import slugify
from django.utils.functional import cached_property
from typing import Tuple, Dict, Any


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(default=None, editable=False)

    def __str__(self) -> str:
        return self.title

    def save(self, *args: Tuple[tuple], **kwargs: Dict[str, any]) -> Any:
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    @cached_property
    def job_count(self) -> int:
        return self.jobs.all().count()


class Job(models.Model):
    title = models.CharField(max_length=300)
    company = models.CharField(max_length=30)
    CHOICES = (
        ('full time', 'Full Time'),
        ('part time', 'Part Time'),
        ('freelance', 'Freelance'),
        ('internship', 'Internship'),
        ('Temporary', 'Temporary'),
    )
    job_type = models.CharField(max_length=30, blank=False, default=None, choices=CHOICES)
    location = models.CharField(max_length=200, blank=False, default=None)
    description = QuillField(blank=False, default=None)
    publishing_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(default=None, editable=False)
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=2)
    employee = models.ManyToManyField(settings.AUTH_USER_MODEL, default=None, blank=True, related_name="Job_Employee")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="jobs", default=1)

    def __str__(self) -> str:
        return self.title

    def save(self, *args: Tuple[tuple], **kwargs: Dict[str, any]) -> Any:
        self.slug = slugify(self.title)
        super(Job, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-id',)
