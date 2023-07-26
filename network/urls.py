
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),    
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("user/<str:usr_name>", views.profile, name="profile"),
    path("edit_profile/<str:username>", views.editProfile, name="edit_profile"),
    path("following", views.display_posts, name="following"),
    path("all", views.redirect, name="index_p"),
    path("<str:path>/page-<int:page_num>", views.load_nthpage, name="following_p"),
    path("<str:path>/<str:usn>/page-<int:page_num>", views.load_nthpage, name="profile_p"),
    # API calls
    path("follow/<str:usr>", views.follow, name="follow"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("like/<int:post_id>", views.like, name="like")
]
