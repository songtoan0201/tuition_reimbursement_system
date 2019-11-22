from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^login$', views.login),
    url(r'^login_page$', views.login_page),
    url(r'^register$', views.register),
    url(r'^register_page$', views.register_page),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout),
    url(r'^employer_registration$', views.employer_registration),
    url(r'^employer_register$', views.employer_register),
]
