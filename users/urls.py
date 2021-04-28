from django.urls import path
from .views import *
from django.contrib.auth import views as authviews

app_name = "users"
urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='update'),
    path('password-change/', authviews.PasswordChangeView.as_view(), name='password_change'),
    path('password-change-done/', authviews.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('employee-detail/<int:job_id>/<int:employee_id>/', EmployeeProfileView.as_view(), name='employee_detail'),
    path('employer-jobs/', EmployerPostedJobsView.as_view(), name='employer_jobs'),
    path('employee-jobs/', EmployeePostedJobsView.as_view(), name='employee_jobs'),
    path('employee-messages/<int:pk>/', EmployeeMessagesView.as_view(), name='employee_messages'),
    path('employee-display-messages/<int:pk>/', EmployeeDisplayMessages.as_view(), name='employee_display_messages'),
    path('add-wishlist/<int:pk>/', AddWishListView.as_view(), name='add_wishlist'),
    path('remove-from-wishlist/<int:pk>/', RemoveFromWishListView.as_view(), name='remove_wishlist'),
    path('mywishlist/<int:pk>/', MyWishList.as_view(), name='my_wish_list'),
]
