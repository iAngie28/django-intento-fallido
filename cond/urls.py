"""
URL configuration for cond project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from condominio import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('mascota/create', views.create_mascota, name="create_mascota"),
    path('mascota/list', views.list_mascota, name="list_mascota"),
    path('mascota/<int:pk>/show', views.show_mascota, name="show_mascota"),
    path('mascota/<int:pk>/delete', views.eliminar_Mascota, name="eliminar_mascota"),

]
