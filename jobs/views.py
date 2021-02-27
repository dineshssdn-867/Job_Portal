from functools import lru_cache
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from blog.models import blog
from happy_blog.models import happy_blog
from jobs.models import Job, Category
from jobs.forms import CreateJob, ApplyJobForm, UpdateJobForm
from users.models import Account, Profile
from typing import Any, Dict, Tuple


@method_decorator(cache_page(60 * 3), name='dispatch')
class HomeView(ListView):
    template_name = 'jobs/index.html'
    model = Job
    context_object_name = 'jobs'
    paginate_by = 3

    @lru_cache(maxsize=None, typed=False)
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super(HomeView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['all_jobs'] = Job.objects.all().count()
        context['candidates'] = Account.objects.filter(is_employee=True).count()
        context['resumes'] = Profile.objects.exclude(resume="").count()
        context['employers'] = Account.objects.filter(is_employer=True).count()
        context['blogs'] = happy_blog.objects.all()
        context['Trend_blogs'] = blog.objects.all()
        return context


@method_decorator(login_required(login_url='/users/login'), name='dispatch')
@method_decorator(cache_page(60 * 3), name='dispatch')
class CreateJobView(SuccessMessageMixin, CreateView):
    model = Job
    template_name = 'jobs/create-jobs.html'
    form_class = CreateJob
    success_url = '/'
    success_message = "Job has been posted"

    def form_valid(self, form: Dict[str, Any]) -> Dict[str, Any]:
        job = form.save(commit=False)
        job.employer = self.request.user
        job.save()
        return super(CreateJobView, self).form_valid(form)


@method_decorator(login_required(login_url='/users/login'), name='dispatch')
@method_decorator(cache_page(60 * 3), name='dispatch')
class SingleJobView(UpdateView, SuccessMessageMixin):
    template_name = 'jobs/single.html'
    model = Job
    context_object_name = 'job'
    form_class = ApplyJobForm
    success_message = "You applied for this job"

    @lru_cache(maxsize=None, typed=False)
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super(SingleJobView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['employee_applied'] = Job.objects.get(pk=self.kwargs['pk']).employee.all().filter(
            id=self.request.user.id)
        try:
            context['applied_employees'] = Job.objects.get(pk=self.kwargs['pk'],
                                                           employer_id=self.request.user.id).employee.all()
            context['employer_id'] = Job.objects.get(pk=self.kwargs['pk']).employer_id
        except:
            pass
        context['all_jobs'] = Job.objects.all().count()
        context['candidates'] = Account.objects.filter(is_employee=True).count()
        context['resumes'] = Profile.objects.exclude(resume="").count()
        context['employers'] = Account.objects.filter(is_employer=True).count()
        context['blogs'] = happy_blog.objects.all()
        context['Trend_blogs'] = blog.objects.all()
        return context

    def form_valid(self, form: Any) -> Dict[str, Any]:
        employee = self.request.user
        form.instance.employee.add(employee)
        form.save()
        return super(SingleJobView, self).form_valid(form)

    def get_success_url(self):
        return reverse('jobs:single_job', kwargs={'slug': self.object.slug, 'pk': self.object.pk})


@method_decorator(login_required(login_url='/users/login'), name='dispatch')
@method_decorator(cache_page(60 * 3), name='dispatch')
class CategoryDetailView(ListView):
    model = Job
    template_name = 'jobs/Category-detail.html'
    context_object_name = 'jobs'
    paginate_by = 2

    @lru_cache(maxsize=None, typed=False)
    def get_queryset(self) -> Any:
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Job.objects.filter(category=self.category)

    @lru_cache(maxsize=None, typed=False)
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        context['categories'] = Category.objects.all()
        context['category'] = self.category
        context['all_jobs'] = Job.objects.all().count()
        context['candidates'] = Account.objects.filter(is_employee=True).count()
        context['resumes'] = Profile.objects.exclude(resume="").count()
        context['employers'] = Account.objects.filter(is_employer=True).count()
        context['blogs'] = happy_blog.objects.all()
        context['Trend_blogs'] = blog.objects.all()
        return context


@method_decorator(login_required(login_url='/users/login'), name='dispatch')
@method_decorator(cache_page(60 * 3), name='dispatch')
class SearchJobView(ListView):
    model = Job
    template_name = 'jobs/search.html'
    context_object_name = 'jobs'
    paginate_by = 2

    @lru_cache(maxsize=None, typed=False)
    def get_queryset(self) -> Dict[str, Any]:
        q1 = self.request.GET.get("job_title")
        q2 = self.request.GET.get("job_type")
        q3 = self.request.GET.get("job_location")

        if q1 and q2 and q3:
            return Job.objects.filter(title__icontains=q1, job_type=q2, location__icontains=q3).order_by('-id')
        elif q1:
            return Job.objects.filter(title__icontains=q1).order_by('-id')
        elif q2:
            return Job.objects.filter(job_type=q2).order_by('-id')
        elif q3:
            return Job.objects.filter(location__icontains=q3).order_by('-id')

        return Job.objects.all().order_by('-id')

    @lru_cache(maxsize=None, typed=False)
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super(SearchJobView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['all_jobs'] = Job.objects.all().count()
        context['candidates'] = Account.objects.filter(is_employee=True).count()
        context['resumes'] = Profile.objects.exclude(resume="").count()
        context['employers'] = Account.objects.filter(is_employer=True).count()
        context['blogs'] = happy_blog.objects.all()
        context['Trend_blogs'] = blog.objects.all()
        return context


@method_decorator(login_required(login_url='/users/login'), name='dispatch')
@method_decorator(cache_page(60 * 3), name='dispatch')
class UpdateJobView(SuccessMessageMixin, UpdateView):
    model = Job
    template_name = 'jobs/update.html'
    form_class = UpdateJobForm
    success_message = "You updated your job!"

    def form_valid(self, form: Any) -> Any:
        form.instance.employer = self.request.user
        return super(UpdateJobView, self).form_valid(form)

    def get(self, request: Any, *args: Tuple[tuple], **kwargs: Dict[str, any]) -> Any:
        self.object = self.get_object()
        if self.object.employer != request.user:
            return HttpResponseRedirect('/')
        return super(UpdateJobView, self).get(request, *args, **kwargs)

    def get_success_url(self) -> Any:
        return reverse('jobs:single_job', kwargs={"pk": self.object.pk, "slug": self.object.slug})


@method_decorator(login_required(login_url='/users/login'), name='dispatch')
@method_decorator(cache_page(60 * 3), name='dispatch')
class DeleteJobView(SuccessMessageMixin, DeleteView):
    model = Job
    success_url = '/'
    template_name = 'jobs/delete.html'

    def delete(self, request: Any, *args: Tuple[tuple], **kwargs: Dict[str, any]) -> Any:
        self.object = self.get_object()
        if self.object.employer == request.user:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        else:
            return HttpResponseRedirect(self.success_url)

    def get(self, request: Any, *args: Tuple[tuple], **kwargs: Dict[str, any]) -> Any:
        self.object = self.get_object()
        if self.object.employer != request.user:
            return HttpResponseRedirect('/')

        return super(DeleteJobView, self).get(request, *args, **kwargs)
