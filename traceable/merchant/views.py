import json

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from utils.jwt import jwt_auth_required
from utils import messages


@csrf_exempt
@jwt_auth_required
def contact_mechanic(request, user=None):
    """
    contact_mechanic view to call the mechanic api
    :param request: http request for the view
        method allowed: POST
        http request should be authorised by the jwt token of the user
        mandatory fields: ['mechanic_api', 'repeat_request_if_failed', 'number_of_repeats']
    :param user: User object of the requesting user
    :returns JsonResponse object with
        response_from_mechanic_api and 200 status if no error
        message and corresponding status if error
    """
    try:
        if request.method != 'POST':
            return JsonResponse({'message': messages.METHOD_NOT_ALLOWED}, status=405)
        user_request_body = json.loads(request.body)
        required_fields = ['mechanic_api', 'repeat_request_if_failed', 'number_of_repeats']
        if not (all(list(field in user_request_body for field in required_fields))) and \
                isinstance(user_request_body['number_of_repeats'], int):
            return JsonResponse({'message': messages.BAD_REQUEST}, status=400)
        if user_request_body['repeat_request_if_failed'] and \
                user_request_body['number_of_repeats'] > 100:
            return JsonResponse({'message': messages.NO_OF_REPEATS_EXCEEDED}, status=503)
        count = 0
        while True:
            print("Repeat count: {}".format(count))
            mechanic_response = requests.get(
                url=user_request_body['mechanic_api'],
                params=user_request_body,
                headers={'Authorization': request.META.get('HTTP_AUTHORIZATION')}
            )
            if mechanic_response.status_code == 200:
                print("Got a valid response at repeat count: {}".format(count))
                break
            if not user_request_body['repeat_request_if_failed']:
                break
            if count == user_request_body['number_of_repeats']:
                break
            count = count + 1
        mechanic_response_status = mechanic_response.status_code
        try:
            mechanic_response = mechanic_response.json()
        except ValueError:
            mechanic_response = mechanic_response.text
        return JsonResponse({
            'response_from_mechanic_api': mechanic_response,
            'status': mechanic_response_status
        }, status=mechanic_response_status)
    except Exception as error:
        return JsonResponse({'message': str(error), 'status': 500}, status=500)
