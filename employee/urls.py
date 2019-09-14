from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url('dashboard', views.dashboard),
    url('customer',views.customer),
    url('register',views.register),
    url('totalsale',views.totalsale),
    url('existing',views.existing)
]