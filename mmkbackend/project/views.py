from django.shortcuts import render
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from project.models import *
import base64
from django.core.cache import cache
# from django_ratelimit.decorators import ratelimit
from .utilities import enforce_rate_limit

# Create your views here.
def default(request):
    return HttpResponse("Hello Welcome!")

@csrf_exempt
def apiOne(request):
    if request.method == 'POST':
        to_params=False
        from_params=False
        try:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2 and auth[0].lower() == 'basic':
                username, password = base64.b64decode(auth[1]).decode().split(':')
                if username and password:
                    check_user = Account.objects.filter(username=username,auth_id=password)
                    if not check_user:
                        return JsonResponse({"message": "authentication is failing", "status_code":'403'})
                else:
                    return JsonResponse({"message": "authentication is failing", "status_code":'403'})
            else:
                return JsonResponse({"message": "authentication is failing", "status_code":'403'})
           
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            to_param = body['to'] if body['to']  else  ''
            if 6<=len(to_param)<=16 :
                check_to_param = Phone_number.objects.filter(number=int(to_param))
                if check_to_param:
                    to_params = True
                else:
                    return JsonResponse({"message": "", "error": "to param is not found"})
            else:
                return JsonResponse({"message": "", "error": "to param is invalid"})

            from_param = body['from']  if  body['from'] else  ''
            if 6<=len(from_param)<=16:
                check_to_param = Phone_number.objects.filter(number=from_param)
                if from_param:
                    from_params = True
                else:
                    return JsonResponse({"message": "", "error": "to param is not found"})
            else:
                return JsonResponse({"message": "", "error": "to param is invalid"})

            text = body['text']  if  body['text'] else  ''
            if 1<=len(text)<=120 and from_params and to_params:
                  if "STOP".strip() in text:
                    cache.set('to',to_param,timeout=5000)
                    cache.set('from',from_param,timeout=5000)
                  return JsonResponse({"message": "inbound sms ok", "error": ""})               
            else:
                return JsonResponse({"message": "", "error": "to param is invalid"})
        except Exception as e:
            return JsonResponse({'message': '', 'error':'unknown failure'})
    else:
        return JsonResponse({'message':'method not Allowed', 'status_code': '405'})
    
@csrf_exempt
def apiTwo(request):
    if not enforce_rate_limit(request):
        return JsonResponse({'message': "","error":f"""limit reached for from """ })
    if request.method == 'POST':
        to_params=False
        from_params=False
        try:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2 and auth[0].lower() == 'basic':
                username, password = base64.b64decode(auth[1]).decode().split(':')
                if username and password:
                    check_user = Account.objects.filter(username=username,auth_id=password)
                    if not check_user:
                        return JsonResponse({"message": "authentication is failing", "status_code":'403'})
                else:
                    return JsonResponse({"message": "authentication is failing", "status_code":'403'})
            else:
                return JsonResponse({"message": "authentication is failing", "status_code":'403'})
           
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            to_param = body['to'] if body['to']  else  ''
            if 6<=len(to_param)<=16 :
                check_to_param = Phone_number.objects.filter(number=int(to_param))
                if check_to_param:
                    to_params = True
                else:
                    return JsonResponse({"message": "", "error": "to param is not found"})
            else:
                return JsonResponse({"message": "", "error": "to param is invalid"})

            from_param = body['from']  if  body['from'] else  ''
            if 6<=len(from_param)<=16:
                check_to_param = Phone_number.objects.filter(number=from_param)
                if from_param:
                    from_params = True
                else:
                    return JsonResponse({"message": "", "error": "to param is not found"})
            else:
                return JsonResponse({"message": "", "error": "to param is invalid"})

            text = body['text']  if  body['text'] else  ''
            if 1<=len(text)<=120 and from_params and to_params:
                  check_to_cache = cache.get('to')
                  check_from_cache = cache.get('from')
                  if check_to_cache and check_from_cache:
                      return JsonResponse({"message": "", "error": f"""sms from {from_param} to {to_param} blocked by STOP request"""})  
                  else:
                    return JsonResponse({"message": "outbound sms ok", "error": ""})            
            else:
                return JsonResponse({"message": "", "error": "to param is invalid"})
        except Exception as e:
            return JsonResponse({'message': '', 'error':'unknown failure'})
    else:
        return JsonResponse({'message':'method not Allowed', 'status_code': '405'})