"""certificate_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from certificate import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view),
     path('create/', views.create_certificate, name='create_certificate'),
    path('view/<int:certificate_id>/', views.view_certificate, name='view_certificate'),
    path('verify/', views.verify_certificate, name='verify_certificate'),
    path('generate_pdf/<int:certificate_id>/', views.generate_pdf, name='generate_pdf'),
]
