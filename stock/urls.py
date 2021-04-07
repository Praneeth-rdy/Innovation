# Django Imports
from django.urls import path, include

# Standard Package Imports

# Project Imports
from . import views


# Third Party Imports


app_name = 'stock'

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.risk_return, name='risk-return'),
    # path('get_quote/', views.get_quote, name='get_quote'),
    # path('<int:year>/', views.diary),
    # path('<int:year>/<str:name>/', views.diary),
]