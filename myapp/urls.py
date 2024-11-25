from django.urls import path
from . import views

urlpatterns = [
    path('register-company/', views.register_company_view, name='register_company'),
    path('edit_company/', views.edit_company_view, name='edit_company'),
    path('delete_company/', views.delete_company_view, name='delete_company'),
   
   
    path('add-product/', views.add_product_view, name='add_product'),
    path('edit_product/', views.edit_product_view, name='edit_product'),
    path('delete_product/', views.delete_product_view, name='delete_product'),


    path('company-details/<int:company_id>/', views.get_company_details_view, name='company_details'),
    path('total-companies/', views.get_total_companies_view, name='total_companies'),
]
