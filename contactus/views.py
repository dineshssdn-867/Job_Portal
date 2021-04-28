from django.views.generic import TemplateView
from jobs.views import CacheMixin


class ContactUsView(TemplateView, CacheMixin):
    template_name = 'Contact_us/Contactus.html'
