"""
shop URL Configuration
The `urlpatterns` list routes URLs to views.
"""
from django.conf.urls import url

import traceable.shop.views as shop_views

urlpatterns = [
    url(r'products', shop_views.products),
    url(r'orders/(?P<order_id>\d+)', shop_views.order_controller),
    url(r'orders/all', shop_views.get_all_order),
    url(r'orders/return_order', shop_views.return_order),
    url(r'orders', shop_views.order_controller),
    url(r'apply_coupon', shop_views.apply_coupon),
]
