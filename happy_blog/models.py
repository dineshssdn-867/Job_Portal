from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _


class happy_blog(models.Model):
    name = models.CharField(_('Name'),max_length=200)
    job_type = models.CharField(_('Job Type'), max_length=300)
    tweet = RichTextField(_('Resume'), blank=True, max_length=300)
    image = models.ImageField(_('image'), upload_to="media/happy_blog", default="media/happy_blog/images.png")
