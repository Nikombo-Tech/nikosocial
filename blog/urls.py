from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("accounts/login", login_view, name="login"),
    path("accounts/logout", logout_view, name="logout"),
    path("accounts/register", register_view, name="register"),
    path("profile", profile_view, name="profile"),

    # Post URLs
    path("posts/", post_list_view, name="post_list"),  # List all posts
    path("posts/create/", post_create_view, name="post_create"), 
    path("posts/<slug:slug>/", post_detail_view, name="post_detail"),  # View a single post # Create a new post
    path("posts/<slug:slug>/delete/", post_delete_view, name="post_delete"),  # Delete a post

    path("posts/<slug:post_slug>/comment/", comment_create_view, name="comment_create"),  # Create a comment
    path("comments/<int:comment_id>/delete/", comment_delete_view, name="comment_delete"),  # Delete a comment

    path("analytics/", analytics_view, name="analytics"),  # Analytics page
]