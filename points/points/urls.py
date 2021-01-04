"""points URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from pages.views import home_page, point_submission,request_submitted, pending_requests
from pages.views import review_task, result, view_points, invalid_password_warning
from pages.views import lapse_of_judgement

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page), 
    path('submit_points/', point_submission),
    path('request_submitted', request_submitted),
    path('pending_requests', pending_requests),
    path('review_task', review_task),
    path('result', result),
    path('view_points', view_points),
    path('invalid_password/', invalid_password_warning),
    path('invalid_alarms', lapse_of_judgement),
]