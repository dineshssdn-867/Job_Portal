from django.db import models
from django.utils.translation import gettext_lazy as _
from django_quill.fields import QuillField


class happy_blog(models.Model):
    name = models.CharField(_('Name'),max_length=200)
    job_type = models.CharField(_('Job Type'), max_length=300)
    tweet = QuillField(_('Resume'), blank=True, max_length=300)
    image = models.ImageField(_('image'), upload_to="media/happy_blog", default="media/happy_blog/images.png")
