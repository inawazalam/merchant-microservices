import json
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from utils.jwt import jwt_auth_required
from utils import messages
from traceable.shop.models import Order, Product, AppliedCoupon
from user.models import UserDetails


@csrf_exempt
@jwt_auth_required
def products(request, user=None):
    """
    products view for adding new product and fetching the list of products
    :param request: http request for the view
        method allowed: GET, POST
        http request should be authorised by the jwt token of the user
        mandatory fields for POST and PUT http methods: ['name', 'price']
    :param user: User object of the requesting user
    :returns JsonResponse object with
        products list and 200 status if no error
        message and corresponding status if error
    """
    try:
        if request.method == 'GET':
            user_details = UserDetails.objects.get(user=user)
            return JsonResponse({
                'products': list(map(lambda a: a.to_dict(), Product.objects.all())),
                'credit': user_details.available_credit,
            })
        if request.method == 'POST':
            user_request_body = request.POST
            required_fields = ['name', 'price', 'image_url']
            if not all(list(field in user_request_body for field in required_fields)):
                return JsonResponse({'message': messages.BAD_REQUEST}, status=400)
            product = Product(
                name=user_request_body['name'],
                price=float(user_request_body['price']),
                image_url=user_request_body['image_url']
            )
            product.save()
            return JsonResponse({'message': messages.PRODUCT_SAVED.format(product.id)})
        return JsonResponse({'message': messages.METHOD_NOT_ALLOWED}, status=405)
    except Exception as error:
        return JsonResponse({'message': str(error), 'status': 500}, status=500)


@csrf_exempt
@jwt_auth_required
def order_controller(request, order_id=None, user=None):
    """
    order view for creating an order
    :param request: http request for the view
        method allowed: POST, GET, PUT
        http request should be authorised by the jwt token of the user
        mandatory fields for POST and PUT http methods: ['product_id', 'quantity']
    :param order_id:
        order_id of the order referring to
        mandatory for GET and PUT http methods
    :param user: User object of the requesting user
    :returns JsonResponse object with
        order object and 200 status if no error
        message and corresponding status if error
    """
    try:
        if request.method == 'POST':
            user_request_body = json.loads(request.body)
            required_fields = ['product_id', 'quantity']
            if not all(list(field in user_request_body for field in required_fields)):
                return JsonResponse({'message': messages.BAD_REQUEST}, status=400)
            product = Product.objects.get(id=user_request_body['product_id'])
            user_details = UserDetails.objects.get(user=user)
            if user_details.available_credit < product.price:
                return JsonResponse({'message': messages.INSUFFICIENT_BALANCE}, status=400)
            user_details.available_credit -= float(product.price * user_request_body['quantity'])
            new_order = Order(
                user=user,
                product=product,
                quantity=user_request_body['quantity'],
                created_on=timezone.now(),
            )
            new_order.save()
            user_details.save()
            return JsonResponse({
                'message': messages.ORDER_CREATED,
                'credit': user_details.available_credit,
            })
        if request.method == 'PUT':
            user_request_body = json.loads(request.body)
            order = Order.objects.get(id=order_id)
            if user != order.user:
                return JsonResponse({'message': messages.RESTRICTED}, status=403)
            if 'quantity' in user_request_body:
                order.quantity = user_request_body['quantity']
            if 'status' in user_request_body and user_request_body['status'] not in [Order.DEL, Order.RET_PEN, Order.RET]:
                return JsonResponse({'message': messages.INVALID_STATUS}, status=400)
            user_details = UserDetails.objects.get(user=order.user)
            if 'status' in user_request_body and user_request_body['status'] != order.status:
                order.status = user_request_body['status']
                if user_request_body['status'] == Order.RET:
                    user_details.available_credit += float(order.quantity * order.product.price)
                    user_details.save()
            order.save()
            return JsonResponse(order.to_dict())
        elif request.method == 'GET':
            order = Order.objects.get(id=order_id)
            if user != order.user:
                return JsonResponse({'message': messages.RESTRICTED}, status=403)
            return JsonResponse(order.to_dict())
        return JsonResponse({'message': messages.METHOD_NOT_ALLOWED}, status=405)
    except Exception as error:
        return JsonResponse({'message': str(error), 'status': 500}, status=500)


@csrf_exempt
@jwt_auth_required
def get_all_order(request, user=None):
    """
    returns all the order of the particular user
    :param request: http request for the view
        method allowed: GET
        http request should be authorised by the jwt token of the user
    :param user: User object of the requesting user
    :returns JsonResponse object with
        list of order object and 200 status if no error
        message and corresponding status if error
    """
    try:
        if request.method != 'GET':
            return JsonResponse({'message': messages.METHOD_NOT_ALLOWED}, status=405)
        return JsonResponse({'orders': list(map(
            lambda a: a.to_dict(),
            Order.objects.filter(user=user)
        ))})
    except Exception as error:
        return JsonResponse({'message': str(error), 'status': 500}, status=500)


@csrf_exempt
@jwt_auth_required
def return_order(request, user=None):
    """
    api for returning an order
    :param request: http request for the view
        method allowed: POST
        http request should be authorised by the jwt token of the user
    :param user: User object of the requesting user
    :returns JsonResponse object with
        message and 200 status if no error
        message and corresponding status if error
    """
    try:
        if request.method != 'POST':
            return JsonResponse({'message': messages.METHOD_NOT_ALLOWED}, status=405)
        order = Order.objects.get(id=request.GET['order_id'])
        print(user)
        print(order.user)
        if user != order.user:
            return JsonResponse({'message': messages.RESTRICTED}, status=403)
        if order.status != Order.DEL:
            return JsonResponse({'message': messages.ORDER_ALREADY_RETURNED}, status=400)
        order.status = Order.RET_PEN
        order.save()
        return JsonResponse({
            'message': messages.ORDER_RETURNING,
            'qr_code_url': messages.QR_CODE_URL,
            'order': order.to_dict()
        })
    except Exception as error:
        return JsonResponse({'message': str(error), 'status': 500}, status=500)


@csrf_exempt
@jwt_auth_required
def apply_coupon(request, user=None):
    """
    api for checking if coupon is already claimed
    if claimed before: returns an error message
    else: increases the user credit
    :param request: http request for the view
        method allowed: POST
        http request should be authorised by the jwt token of the user
    :param user: User object of the requesting user
    :returns JsonResponse object with
        message and 200 status if no error
        message and corresponding status if error
    """
    try:
        if request.method != 'POST':
            return JsonResponse({'message': messages.METHOD_NOT_ALLOWED}, status=405)
        coupon_request_body = json.loads(request.body)
        required_fields = ['couponcode', 'amount']
        if not all(list(field in coupon_request_body for field in required_fields)):
            return JsonResponse({'message': messages.BAD_REQUEST}, status=400)
        try:
            AppliedCoupon.objects.get(user=user, coupon_code=coupon_request_body['couponcode'])
            return JsonResponse({'message': messages.COUPON_ALREADY_APPLIED}, status=400)
        except AppliedCoupon.DoesNotExist:
            coupon = AppliedCoupon(user=user, coupon_code=coupon_request_body['couponcode'])
            user_details = UserDetails.objects.get(user=user)
            user_details.available_credit += float(coupon_request_body['amount'])
            coupon.save()
            user_details.save()
            return JsonResponse({
                'credit': user_details.available_credit,
                'message': messages.COUPON_APPLIED
            })
    except Exception as error:
        return JsonResponse({'message': str(error), 'status': 500}, status=500)
