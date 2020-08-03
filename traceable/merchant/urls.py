"""
merchant URL Configuration
The `urlpatterns` list routes URLs to views.
"""
from django.conf.urls import url

import traceable.merchant.views as merchant_views

urlpatterns = [
    url(r'contact_mechanic', merchant_views.contact_mechanic),
]
