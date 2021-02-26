from functools import lru_cache
from typing import Dict, Any
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, TemplateView
from happy_blog.models import happy_blog
from jobs.models import Job
from users.models import Account, Profile


@method_decorator(cache_page(60 * 3), name='dispatch')
class AboutUsView(TemplateView):
    template_name = 'About_us/aboutus.html'

    @lru_cache(maxsize=None, typed=False)
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super(AboutUsView, self).get_context_data(**kwargs)
        context['all_jobs'] = Job.objects.all().count()
        context['candidates'] = Account.objects.filter(is_employee=True).count()
        context['resumes'] = Profile.objects.exclude(resume="").count()
        context['employers'] = Account.objects.filter(is_employer=True).count()
        context['blogs'] = happy_blog.objects.all()
        return context
