"""
Traceable URL Configuration
The `urlpatterns` list routes URLs to URLConf.
"""
from django.urls import path, include

urlpatterns = [
    path('api/mechanic', include('traceable.mechanic.urls')),
    path('api/merchant', include('traceable.merchant.urls')),
    path('api/shop', include('traceable.shop.urls')),
]
