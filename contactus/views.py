from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView


@method_decorator(cache_page(60 * 3), name='dispatch')
class ContactUsView(TemplateView):
    template_name = 'Contact_us/Contactus.html'
