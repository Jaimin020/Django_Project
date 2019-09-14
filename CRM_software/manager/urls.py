from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url('dashboard', views.dashboard),
    url('employees', views.display_employees),
    url('customers', views.display_customers),
    url('products', views.display_products),
    url('emailemployee', views.sendEmailEmp),
    url('emailcustomer', views.sendEmailCus),
    url('registerProduct', views.register_product),
]