from django.urls import path
from .views import *

urlpatterns = [
    path('',login_view, name='login'),
    path('entry/', login_or_singin_event, name='login_or_singin_event'),
    path('post_user_input/', post_user_input, name='post_user_input'),
    path('mypage/', user_home_view, name='user_home'),
    path('buildtask/', build_task_view, name='buildtask'),
    path('post_build_task_input/', post_build_task_input, name='post_build_task_input'),
    path('post_line_message/', post_line_message, name='post_line_message')
]