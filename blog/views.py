from functools import lru_cache
from typing import Any, Dict
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, CreateView
from blog.forms import BlogForm
from blog.models import blog


class BlogView(ListView):
    template_name = 'Blog/blog.html'
    model = blog
    context_object_name = 'blogs'
    paginate_by = 3


@method_decorator(cache_page(60 * 3), name='dispatch')
@method_decorator(login_required(login_url='/users/login'), name='dispatch')
class AddBlogView(CreateView):
    template_name = 'blog/add-blog.html'
    model = blog
    form_class = BlogForm

    def form_valid(self, form: Any) -> Dict[str, Any]:
        instance = form.save(commit=False)
        instance.save()
        return super(AddBlogView, self).form_valid(form)

    def get_success_url(self) -> Any:
        return reverse('blog:Blog')
