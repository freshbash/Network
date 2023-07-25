
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all", views.redirect, name="redirect_to_index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("user/<str:usr_name>", views.profile, name="profile"),
    path("following", views.display_posts, name="following"),
    path("page-<int:page_num>", views.load_nthpage, name="for_all_posts"),
    path("<str:path>/page-<int:page_num>", views.load_nthpage, name="following_profile"),
    # API calls
    path("follow/<str:usr>", views.follow, name="follow"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("like/<int:post_id>", views.like, name="like")
]
