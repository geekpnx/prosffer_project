from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import login_view, logout_view, signup_view, view_edit_profile_view


app_name = 'user-urls'
urlpatterns = [
  
    path('user/signup/', signup_view, name='signup'),
    path('user/login/', login_view, name='login'),
    path('user/profile/', view_edit_profile_view, name='profile'),
    path('user/logout/', logout_view, name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)