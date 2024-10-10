from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import login_view, logout_view, signup_view, edit_profile_view, welcome_view, view_profile_view, store
from .views.home_page import about_view


# app_name = "user"

urlpatterns = [
    path("", store, name="store"),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("view_profile/", view_profile_view, name="view_profile"),
    path("edit_profile/", edit_profile_view, name="edit_profile"),
    path("welcome/", welcome_view, name="welcome"),
    path("logout/", logout_view, name="logout"),
    path("about/", about_view, name="about"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
