from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import *

urlpatterns = [
                  path('', views.index, name='index'),
                  path('register/', RegisterUser.as_view(), name='register'),
                  path('login/', LoginUser.as_view(), name='login'),
                  path('admin_page/', views.dowload_statistics, name='admin_page'),
                  path('user/get_photo/', views.user_photo, name='get_photo'),
                  path('user/criteria/', views.criteria, name='criteria'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
