from django.db import models
from django.utils.translation import gettext_lazy as _
from django_quill.fields import QuillField


class blog(models.Model):
    name = models.CharField(_('Name'),max_length=200)
    title = models.CharField(_('Title'), max_length=300)
    tweet = QuillField(_('Resume'), blank=True, max_length=500)
    date = models.DateField(_('date'), auto_now_add=True)
    image = models.ImageField(_('image'), upload_to="media/blog", default="media/happy_blog/images.png")
