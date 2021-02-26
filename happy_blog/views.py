from typing import Any, Dict
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView
from happy_blog.forms import HappyBlogForm
from happy_blog.models import happy_blog


# @method_decorator(cache_page(60 * 3), name='dispatch')
@method_decorator(login_required(login_url='/users/login'), name='dispatch')
class HappyBlogView(CreateView):
    template_name = 'happy_blog/happy-blog.html'
    model = happy_blog
    form_class = HappyBlogForm

    def form_valid(self, form: Any) -> Dict[str, Any]:
        instance = form.save(commit=False)
        instance.save()
        return super(HappyBlogView, self).form_valid(form)

    def get_success_url(self) -> Any:
        return reverse('jobs:home')