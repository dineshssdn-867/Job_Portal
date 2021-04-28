from django.urls import path
from happy_blog.views import HappyBlogView

app_name = "happy_blog"
urlpatterns = [
    path('',  HappyBlogView.as_view(), name='happyblog')
]
