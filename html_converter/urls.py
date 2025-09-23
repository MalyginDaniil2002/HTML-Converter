"""
URL configuration for html_converter project.

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
from authentication import views as auth
from account import views as account
from periodic import views as periodic
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="home.html")),
    path('login', auth.log_in),
    path('accounts/login/', auth.nologin),
    path('register', auth.register),
    path('account/', account.account),
    path('account/main', account.main),
    path('account/add', account.add),
    path('account/edit/<int:sheet_id>', account.edit),
    path('account/update/<int:sheet_id>', account.update),
    path('account/remove/<int:sheet_id>', account.remove),
    path('account/delete', account.delete),
    path('show/<str:file_name>', periodic.show),
    path('logout', auth.log_out),
]
