from django.contrib.auth.views import LoginView
from django.urls import path


from .views import (
    AvatarView,
)

app_name = "app_auth"

urlpatterns = [


    path('users/', AvatarView.user_list.as_view(), name='user_list'),
    path('users/<int:pk>/', AvatarView.user_detail.as_view(), name='user_detail'),
    path('users/<int:pk>/update-avatar/', AvatarView.update_avatar.as_view(), name='update_avatar'),

]
