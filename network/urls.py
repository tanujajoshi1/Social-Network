
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>",views.profile,name="profile"),
    path("profile/<str:username>/create",views.create,name="create"),
    path("following/<str:username>",views.following,name="following"),
    path("posts/<int:postID>/edit",views.edit,name="edit"),
    path('like',views.like,name="like")
]
