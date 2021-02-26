from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView


# @method_decorator(cache_page(60 * 3), name='dispatch')
class AboutUsView(TemplateView):
    template_name = 'About_us/aboutus.html'
