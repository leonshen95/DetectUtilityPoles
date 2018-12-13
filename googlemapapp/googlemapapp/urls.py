from django.conf.urls.static import static
from . import settings
from django.contrib import admin
from django.urls import path
from test_nov6 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('index/', views.index),
    path('map/', views.map),
    path('sign-up/', views.sign_up),
    path('add_user/', views.add_user),
    path('show_user/', views.show_user),
]
urlpatterns += static('/upload/', document_root=settings.MEDIA_ROOT)