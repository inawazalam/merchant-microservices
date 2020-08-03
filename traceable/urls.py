from django.conf.urls import url
from traceable.views import merchant_controller

urlpatterns = [
   url(r'^merchants/', merchant_controller, name='merchant'),
]