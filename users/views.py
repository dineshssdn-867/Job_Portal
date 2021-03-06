from functools import lru_cache
from typing import Dict, Any, Tuple
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from blog.models import blog
from happy_blog.models import happy_blog
from jobs.models import Category, Job
from users.forms import *
from users.models import Profile, Account


@method_decorator(cache_page(60 * 0.5), name='dispatch')
class UserRegisterView(SuccessMessageMixin, CreateView):
    model = Account
    template_name = 'users/user-register.html'
    form_class = AccountRegisterForm
    success_url = '/'
    success_message = "Your user account has been created!"

    def form_valid(self, form: Any) -> Dict[str, Any]:
        user = form.save(commit=False)
        user_type = form.cleaned_data['user_types']
        if user_type == 'is_employee':
            user.is_employee = True
        elif user_type == 'is_employer':
            user.is_employer = True

        user.save()
        return redirect(self.success_url)


@method_decorator(cache_page(60 * 0.5), name='dispatch')
class UserLoginView(LoginView):
    template_name = 'users/login.html'


@method_decorator(cache_page(60 * 0.5), name='dispatch')
class UserLogoutView(LogoutView):
    template_name = 'users/login.html'


@method_decorator(login_required(login_url='/users/login'), name='dispatch')
@method_decorator(cache_page(60 * 0.5), name='dispatch')
class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = Profile
    success_message = 'You updated your profile'
    template_name = 'users/update.html'
    form_class = UserUpdateform

    def form_valid(self, form: Any) -> Dict[str, Any]:
        form.instance.user = self.request.user
        return super(UserUpdateView, self).form_valid(form)

    def get(self, request: Any, *args: Tuple[tuple], **kwargs: Dict[str, any]) -> Any:
        self.object = self.get_object()
        if self.object.user != request.user:
            return HttpResponseRedirect('/')
        return super(UserUpdateView, self).get(request, *args, **kwargs)

    def get_success_url(self) -> Any:
        return reverse('users:update', kwargs={'pk': self.object.pk})


@method_decorator(login_required(login_url='/users/login'), name='dispatch')
@method_decorator(cache_page(60 * 0.5), name='dispatch')
class EmployeeProfileView(CreateView):
    template_name = 'users/employee-profile.html'
    model = Account
    form_class = InviteEmployeeform

    @lru_cache(maxsize=None, typed=False)
    def get_context_data(self, **kwargs: Dict[str, any]) -> Dict[str, Any]:
        context = super(EmployeeProfileView, self).get_context_data(**kwargs)
        context['account'] = Account.objects.get(pk=self.kwargs['employee_id'])
        context['profile'] = Profile.objects.get(user_id=self.kwargs['employee_id'])
        context['job'] = Job.objects.get(id=self.kwargs['job_id'])
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form: Any) -> Dict[str, Any]:
        instance = form.save(commit=False)
        instance.user = Account.objects.get(pk=self.kwargs['employee_id'])
        instance.job = Job.objects.get(id=self.kwargs['job_id'])
        instance.save()
        return super(EmployeeProfileView, self).form_valid(form)

    def get_success_url(self) -> Any:
        return reverse('users:employer_jobs')


@method_decorator(cache_page(60 * 0.5), name='dispatch')
@method_decorator(login_required(login_url='/users/login'), name='dispatch')
class EmployerPostedJobsView(ListView):
    template_name = 'users/employer-posted-jobs.html'
    model = Job
    paginate_by = 2
    context_object_name = 'employer_jobs'

    @lru_cache(maxsize=None, typed=False)
    def get_queryset(self) -> Tuple[Tuple]:
        return Job.objects.filter(employer=self.request.user).order_by('-id')

    @lru_cache(maxsize=None, typed=False)
    def get_context_data(self, **kwargs: Dict[str, any]) -> Dict[str, Any]:
        context = super(EmployerPostedJobsView, self).get_context_data(**kwargs)
        context['all_jobs'] = Job.objects.all().count()
        context['candidates'] = Account.objects.filter(is_employee=True).count()
        context['resumes'] = Profile.objects.exclude(resume="").count()
        context['employers'] = Account.objects.filter(is_employer=True).count()
        context['blogs'] = happy_blog.objects.all()
        context['Trend_blogs'] = blog.objects.all()
        return context


@method_decorator(cache_page(60 * 0.5), name='dispatch')
@method_decorator(login_required(login_url='/users/login'), name='dispatch')
class EmployeeMessagesView(ListView):
    template_name = 'users/employee-messages.html'
    model = Job
    paginate_by = 2
    context_object_name = 'jobs'

    def get_queryset(self) -> Tuple[Tuple]:
        return Job.objects.filter(invites__isnull=False, invites__user_id=self.request.user).order_by('-invites')

    @lru_cache(maxsize=None, typed=False)
    def get_context_data(self, **kwargs: Dict[str, any]) -> Dict[str, Any]:
        context = super(EmployeeMessagesView, self).get_context_data(**kwargs)
        context['all_jobs'] = Job.objects.all().count()
        context['candidates'] = Account.objects.filter(is_employee=True).count()
        context['resumes'] = Profile.objects.exclude(resume="").count()
        context['employers'] = Account.objects.filter(is_employer=True).count()
        context['blogs'] = happy_blog.objects.all()
        context['Trend_blogs'] = blog.objects.all()
        return context


@method_decorator(login_required(login_url='/users/login'), name='dispatch')
@method_decorator(cache_page(60 * 0.5), name='dispatch')
class EmployeeDisplayMessages(DetailView):
    model = Invite
    template_name = 'users/employee-display-messages.html'
    context_object_name = 'invite'

    def get_queryset(self) -> Tuple[Tuple]:
        invite = self.model.objects.filter(id=self.kwargs['pk'])
        invite.update(unread=False)
        return invite

    def get(self, request: Any, *args: Tuple[tuple], **kwargs: Dict[str, any]) -> Any:
        self.object = self.get_object()
        if self.object.user != request.user:
            return HttpResponseRedirect('/')
        return super(EmployeeDisplayMessages, self).get(request, *args, **kwargs)


@method_decorator(login_required(login_url='/users/login'), name='dispatch')
@method_decorator(cache_page(60 * 0.5), name='dispatch')
class AddWishListView(UpdateView):
    template_name = 'jobs/index.html'
    model = Profile

    def get(self, request: Any, *args: Tuple[tuple], **kwargs: Dict[str, any]) -> Any:
        if self.request.user.is_employee:
            job = Job.objects.get(id=self.kwargs['pk'])
            profile = Profile.objects.get(user=request.user)
            profile.wish_list.add(job)
            return redirect('jobs:home')

        else:
            return redirect('jobs:home')


@method_decorator(login_required(login_url='/users/login'), name='dispatch')
@method_decorator(cache_page(60 * 0.5), name='dispatch')
class RemoveFromWishListView(UpdateView):
    template_name = 'jobs/index.html'
    model = Profile

    def get(self, request: Any, *args: Tuple[tuple], **kwargs: Dict[str, any]) -> Any:
        if self.request.user.is_employee:
            job = Job.objects.get(id=self.kwargs['pk'])
            profile = Profile.objects.get(user=request.user)
            profile.wish_list.remove(job)
            return redirect('jobs:home')

        else:
            return redirect('jobs:home')


@method_decorator(login_required(login_url='/users/login'), name='dispatch')
@method_decorator(cache_page(60 * 0.5), name='dispatch')
class MyWishList(ListView):
    template_name = 'users/my-wish-list.html'
    context_object_name = 'jobs'
    model = Job
    paginate_by = 5

    def get_queryset(self) -> Tuple[Tuple]:
        return Job.objects.filter(wish_list__user_id=self.request.user.id)

    @lru_cache(maxsize=None, typed=False)
    def get_context_data(self, **kwargs: Dict[str, any]) -> Dict[str, Any]:
        context = super(MyWishList, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['wish_list'] = Job.objects.filter(wish_list__user_id=self.request.user.id).values_list('id',
                                                                                                           flat=True)
        context['all_jobs'] = Job.objects.all().count()
        context['candidates'] = Account.objects.filter(is_employee=True).count()
        context['resumes'] = Profile.objects.exclude(resume="").count()
        context['employers'] = Account.objects.filter(is_employer=True).count()
        context['blogs'] = happy_blog.objects.all()
        return context


@method_decorator(cache_page(60 * 0.5), name='dispatch')
@method_decorator(login_required(login_url='/users/login'), name='dispatch')
class EmployeePostedJobsView(ListView):
    template_name = 'users/employee-posted-jobs.html'
    model = Job
    paginate_by = 2
    context_object_name = 'employee_jobs'

    def get_queryset(self) -> Tuple[Tuple]:
        return Job.objects.filter(employee=self.request.user).order_by('-id')

    @lru_cache(maxsize=None, typed=False)
    def get_context_data(self, **kwargs: Dict[str, any]) -> Dict[str, Any]:
        context = super(EmployeePostedJobsView, self).get_context_data(**kwargs)
        context['all_jobs'] = Job.objects.all().count()
        context['candidates'] = Account.objects.filter(is_employee=True).count()
        context['resumes'] = Profile.objects.exclude(resume="").count()
        context['employers'] = Account.objects.filter(is_employer=True).count()
        context['blogs'] = happy_blog.objects.all()
        context['Trend_blogs'] = blog.objects.all()
        return context
