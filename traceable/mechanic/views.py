import json
import bcrypt
from django.utils import timezone
from django.db import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from utils.jwt import jwt_auth_required
from utils import messages
from user.models import User, Vehicle, UserDetails
from .models import Mechanic, ServiceRequest


@csrf_exempt
def signup(request):
    """
    creates a new Mechanic in the db
    :param request: http request for the view
        method allowed: POST
        mandatory fields: ['name', 'email', 'number', 'password', 'mechanic_code']
    :returns JsonResponse object with
        mechanics list and 200 status if no error
        message and corresponding status if error
    """
    try:
        if request.method != 'POST':
            return JsonResponse({'message': messages.METHOD_NOT_ALLOWED}, status=405)
        mechanic_details = json.loads(request.body)
        required_fields = ['name', 'email', 'number', 'password', 'mechanic_code']
        if not all(list(field in mechanic_details for field in required_fields)):
            return JsonResponse({'message': messages.BAD_REQUEST}, status=400)
        if mechanic_details['email'] in map(lambda a: a.email, User.objects.all()):
            return JsonResponse({'message': messages.EMAIL_ALREADY_EXISTS}, status=400)
        if mechanic_details['mechanic_code'] in map(
                lambda a: a.mechanic_code,
                Mechanic.objects.all()
        ):
            return JsonResponse({'message': messages.MEC_CODE_ALREADY_EXISTS}, status=400)
        try:
            user_id = User.objects.aggregate(models.Max('id'))['id__max'] + 1
        except TypeError:
            user_id = 1
        user = User.objects.create(
            id=user_id,
            email=mechanic_details['email'],
            number=mechanic_details['number'],
            password=bcrypt.hashpw(
                mechanic_details['password'].encode('utf-8'),
                bcrypt.gensalt()
            ).decode(),
            role=User.MECH,
            created_on=timezone.now()
        )
        Mechanic.objects.create(
            mechanic_code=mechanic_details['mechanic_code'],
            user=user
        )
        try:
            user_details_id = UserDetails.objects.aggregate(models.Max('id'))['id__max'] + 1
        except TypeError:
            user_details_id = 1
        UserDetails.objects.create(
            id=user_details_id,
            available_credit=0,
            name=mechanic_details['name'],
            status='ACTIVE',
            user=user
        )
        return JsonResponse({'message': messages.MEC_CREATED.format(user.email)})
    except Exception as error:
        return JsonResponse({'message': str(error)}, status=500)


@csrf_exempt
@jwt_auth_required
def get_mechanic(request, user=None):
    """
    get_mechanic view for fetching the list of mechanics
    :param request: http request for the view
        method allowed: GET
        http request should be authorised by the jwt token of the user
    :param user: User object of the requesting user
    :returns JsonResponse object with
        mechanics list and 200 status if no error
        message and corresponding status if error
    """
    try:
        if request.method != 'GET':
            return JsonResponse({'message': messages.METHOD_NOT_ALLOWED}, status=405)
        return JsonResponse({'mechanics': list(map(lambda a: a.to_dict(), Mechanic.objects.all()))})
    except Exception as error:
        return JsonResponse({'message': str(error), 'status': 500}, status=500)


@csrf_exempt
def receive_report(request):
    """
    receive_report endpoint for mechanic
    :param request: http request for the view
        method allowed: POST
        mandatory fields: ['mechanic_code', 'problem_details', 'vin']
    :returns JsonResponse object with
        { service request id, report link } and 200 status if no error
        message and corresponding status if error
    """
    try:
        if request.method == 'GET':
            report_details = request.GET
            required_fields = ['mechanic_code', 'problem_details', 'vin']
            if not all(list(field in report_details for field in required_fields)):
                return JsonResponse({'message': messages.BAD_REQUEST}, status=400)
            mechanic = Mechanic.objects.get(mechanic_code=report_details['mechanic_code'])
            vehicle = Vehicle.objects.get(vin=report_details['vin'])
            service_request = ServiceRequest(
                vehicle=vehicle,
                mechanic=mechanic,
                problem_details=report_details['problem_details'],
                created_on=timezone.now()
            )
            service_request.save()
            report_link = "/api/mechanic/mechanic_report?report_id={}".format(service_request.id)
            return JsonResponse({
                'id': service_request.id,
                'sent': True,
                'report_link': report_link
            })
        return JsonResponse({'message': messages.METHOD_NOT_ALLOWED}, status=405)
    except Exception as error:
        return JsonResponse({'message': str(error), 'status': 400}, status=400)


@csrf_exempt
def get_report(request):
    """
    fetch service request details from report_link
    :param request: http request for the view
        method allowed: GET
    :returns JsonResponse object with
        service request object and 200 status if no error
        message and corresponding status if error
    """
    try:
        if request.method == 'GET' and 'report_id' in request.GET:
            return JsonResponse(
                ServiceRequest.objects.get(id=int(request.GET['report_id'])).to_dict()
            )
        return JsonResponse({'message': messages.BAD_REQUEST}, status=400)
    except Exception as error:
        return JsonResponse({'message': str(error), 'status': 400}, status=400)


@csrf_exempt
@jwt_auth_required
def get_service_requests(request, user=None):
    """
    fetch all service requests assigned to the particular mechanic
    :param request: http request for the view
        method allowed: GET
        http request should be authorised by the jwt token of the mechanic
    :param user: User object of the requesting user
    :returns JsonResponse object with
        list of service request object and 200 status if no error
        message and corresponding status if error
    """
    try:
        if request.method != 'GET':
            return JsonResponse({'message': messages.METHOD_NOT_ALLOWED}, status=405)
        mechanic = Mechanic.objects.filter(user=user)[0]
        service_requests = ServiceRequest.objects.filter(mechanic=mechanic)
        return JsonResponse({
            'service_requests': list(map(lambda a: a.to_dict(), service_requests))
        })
    except Exception as error:
        return JsonResponse({'message': str(error), 'status': 500}, status=500)
