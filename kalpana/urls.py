"""kalpana URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/API/', app_views.login_user_api, name='login_api'),
    path('register/API/', app_views.register_user_api, name='register_api'),
    path('note/new/', app_views.create_new_note, name='create_new_note'),
    path('note/update/', app_views.update_note, name='update_note'),
    path('', app_views.get_notes, name='get_notes')
]
