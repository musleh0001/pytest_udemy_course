from django.urls import path
from rest_framework import routers

from .views import CompanyViewSet

companies_router = routers.DefaultRouter()
companies_router.register('Companies', viewset=CompanyViewSet, basename='companies')