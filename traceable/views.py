from django.http import JsonResponse
from .models import Merchant
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def merchant_controller(request):
    if request.method == 'GET':
        return JsonResponse({'merchants': list(map(lambda a: a.to_dict(), Merchant.objects.all()))})
    # if request.method == 'POST':
    #     print(json.loads(request.body))
    #     return JsonResponse({'merchants': list(map(lambda a: a.to_dict(), Merchant.objects.all()))})
