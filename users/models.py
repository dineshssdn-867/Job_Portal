from PIL import Image
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from typing import Dict, Any, Tuple


from django_quill.fields import QuillField

from jobs.models import Job


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email: str, password: str, **extra_fields: Dict[str, Any]) -> Dict[str, Any]:
        if not email:
            raise ValueError('Your email is not correct')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str = None, **extra_fields: Dict[str, Any]) -> Dict[str, Any]:
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str = None, **extra_fields: Dict[str, Any]) -> Any:
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=50, blank=False)
    last_name = models.CharField(_('last name'), max_length=50, blank=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('is_staff'), default=False)
    is_employee = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    @cached_property
    def count_unread_messages(self) -> int:
        return self.invites.filter(unread=True).count()

    @cached_property
    def get_profile_id(self) -> int:
        return self.profile.id

    @cached_property
    def unread_messages(self) -> int:
        return self.invites.filter(unread=True).values_list('job_id', flat=True)


class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(_('image'), upload_to="users/", default="job_portal/users/images_n40np7.png")
    birth_day = models.DateField(_('birth_day'), default=None, blank=True, null=True)
    location = models.CharField(_('location'), max_length=100, blank=True)
    resume = QuillField(_('Resume'), blank=True)
    company = models.CharField(_('company'), max_length=250, blank=True)
    wish_list = models.ManyToManyField(Job, default=None, blank=True, related_name="wish_list")

    def __str__(self) -> str:
        return self.user.first_name + " " + self.user.last_name + " " + self.user.email


@receiver(models.signals.post_save, sender=Account)
def post_save_user_signal(sender: Any, instance: Any, created: Any, **kwargs: Dict[str, any]) -> Any:
    if created:
        instance.save()


def create_user_profile(sender: Any, instance: Any, created: Any, **kwargs: Dict[str, any]) -> Any:
    if created:
        Profile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=Account)


class Invite(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="invites")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="invites", default=1)
    date = models.DateField(default=None, blank=True, null=True)
    message = QuillField(blank=True)
    unread = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.job.title
