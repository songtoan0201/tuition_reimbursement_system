from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^application$', views.application),
    url(r'^new_application$', views.new_application),
    url(r'^employee_application$', views.employee_application),
    url(r'^view_application/(?P<application_id>\d+)$$', views.view_application),
    url(r'^review_application/(?P<application_id>\d+)$$', views.review_application),
    url(r'^revise_application/(?P<application_id>\d+)$$', views.revise_application),
    url(r'^account$', views.account),
    url(r'^employer_account$', views.employer_account),
    url(r'^edit_account$', views.edit_account),
    url(r'^edit_employer_account$', views.edit_employer_account),
    url(r'^delete_application/(?P<application_id>\d+)$',views.delete_application),
    url(r'^edit_application/(?P<application_id>\d+)$',views.edit_application),
    url(r'^viewaccount$', views.account),
    url(r'^contact$', views.contact),
    url(r'^submit_request$', views.submit_request),
]
