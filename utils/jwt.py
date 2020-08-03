"""
Contains all the methods related to jwt token
"""
from datetime import datetime, timedelta
from functools import wraps

import jwt
from django.conf import settings
from django.http import JsonResponse
from utils import messages
from user.models import User


# def get_username(request):
#     """
#     :param request: http request
#         http request should be authorised by the jwt token of the user
#     :returns username(str) encoded in the jwt token
#     """
#     if request.META.get('HTTP_AUTHORIZATION')[0:7] == 'Bearer ':
#         token = request.META.get('HTTP_AUTHORIZATION')[7:]
#         decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS512'])
#         return decoded['sub']
#     return False


def get_jwt(user, exp=None):
    """
    returns a jwt token from User object
    :param user: user object
    :param exp: expiry date and time for jwt
                if not mentioned, 3 hours from iat
    :return: jwt token as a string
    """
    pay_load = {
        'sub': user.email,
        'iat': datetime.now(),
        'exp': exp or (datetime.now() + timedelta(hours=3))
    }
    encoded = jwt.encode(pay_load, settings.JWT_SECRET, algorithm='HS512')
    return encoded.decode("utf-8")


def jwt_auth_required(func):
    """
    decorator for authorizing http requests
    :param func: view function of the api
    :return: a new view function which
        calls the actual view function if authorized
        returns error message if not authorized
    """
    @wraps(func)
    def new_func(*args, **kwargs):
        try:
            request = args[0]
            if 'HTTP_AUTHORIZATION' in request.META \
                    and request.META.get('HTTP_AUTHORIZATION')[0:7] == 'Bearer ':
                token = request.META.get('HTTP_AUTHORIZATION')[7:]
                decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS512'])
                username = decoded['sub']
                user = User.objects.get(email=username)
                kwargs['user'] = user  # Add user object to the view function if authorized
                return func(*args, **kwargs)
            return JsonResponse({'message': messages.JWT_REQUIRED}, status=401)
        except (jwt.exceptions.DecodeError, User.DoesNotExist):
            return JsonResponse({'message': messages.INVALID_TOKEN}, status=401)
        except jwt.exceptions.ExpiredSignatureError:
            return JsonResponse({'message': messages.TOKEN_EXPIRED}, status=401)
    return new_func
