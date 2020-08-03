"""
mechanic URL Configuration
The `urlpatterns` list routes URLs to views.
"""
from django.conf.urls import url

import traceable.mechanic.views as mechanic_views

urlpatterns = [
    url(r'signup', mechanic_views.signup),
    url(r'receive_report', mechanic_views.receive_report),
    url(r'mechanic_report', mechanic_views.get_report),
    url(r'service_requests', mechanic_views.get_service_requests),
    url(r'', mechanic_views.get_mechanic),
]
