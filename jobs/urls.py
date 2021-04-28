from django.urls import path

from .views import *

app_name = "jobs"
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('create-job/', CreateJobView.as_view(), name="create_job"),
    path('search/', SearchJobView.as_view(), name="search"),
    path('detail/<slug>/<int:pk>/', SingleJobView.as_view(), name="single_job"),
    path('category-detail/<slug>/<int:pk>/', CategoryDetailView.as_view(), name="category_detail"),
    path('update/<slug>/<int:pk>/', UpdateJobView.as_view(), name="update_job"),
    path('delete/<slug>/<int:pk>/', DeleteJobView.as_view(), name="delete_job"),

]
