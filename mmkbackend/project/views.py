from django.shortcuts import render
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from project.models import *
from django.core.cache import cache
# from django_ratelimit.decorators import ratelimit
from .utilities import check_rate_limit, auth_check, validate_fromparam, validate_toparam

# Create your views here.
def default(request):
    return HttpResponse("Hello Welcome!")

@csrf_exempt
def inboundapi(request):
    if request.method == 'POST':
        to_params=False
        from_params=False
        try:
            # authentication
            authentication = auth_check(request)
            if not authentication:
                return JsonResponse({"message": "authentication is failing"},status=403)
            
            # validating the to_param
            to_param, validation = validate_toparam(request)
            if to_param and validation:
                to_params=True
            else:
                return JsonResponse({"message": "", "error": f"{validation}"})
            # validating the from_param
            from_param, validation = validate_fromparam(request)
            if from_param and validation:
                from_params=True
            else:
                return JsonResponse({"message": "", "error": f"{validation}"})
            
            # text validation
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            to_param = body['to'] if body['to']  else  ''
            from_param = body['from'] if body['from']  else  ''
            text = body['text']  if  body['text'] else  ''
            if 1<=len(text)<=120 and from_params and to_params:
                  if "STOP".strip() in text:
                    cache.set('to',to_param,timeout=40*60*60)
                    cache.set('from',from_param,timeout=40*60*60)
                  return JsonResponse({"message": "inbound sms ok", "error": ""})               
            else:
                return JsonResponse({"message": "", "error": "to param is invalid"})
        except Exception as e:
            return JsonResponse({"message": "", "error":"unknown failure"})
    else:
        return JsonResponse({'message':"method not Allowed"},status=405)
    
@csrf_exempt
def outboundapi(request):
    limit_check,from_param = check_rate_limit(request)
    if not limit_check:
        return JsonResponse({'message': "","error":f"limit reached for from {from_param}" })
    if request.method == 'POST':
        to_params=False
        from_params=False
        try:
            authication = auth_check(request)
            if not authication:
                return JsonResponse({"message": "authentication is failing"},status=403)
            
             # validating the to_param
            to_param, validation = validate_toparam(request)
            if to_param and validation:
                to_params=True
            else:
                return JsonResponse({"message": "", "error": f"{validation}"})
            # validating the from_param
            from_param, validation = validate_fromparam(request)
            if from_param and validation:
                from_params=True
            else:
                return JsonResponse({"message": "", "error": f"{validation}"})
            
            # text validation
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            to_param = body['to'] if body['to']  else  ''
            from_param = body['from'] if body['from']  else  ''
            text = body['text']  if  body['text'] else  ''
            if 1<=len(text)<=120 and from_params and to_params:
                  check_to_cache = cache.get('to')
                  check_from_cache = cache.get('from')
                  if check_to_cache==to_param and check_from_cache==from_param:
                      return JsonResponse({"message": "", "error": f"""sms from {from_param} to {to_param} blocked by STOP request"""})  
                  else:
                    return JsonResponse({"message": "outbound sms ok", "error": ""})            
            else:
                return JsonResponse({"message": "", "error": "to param is invalid"})
        except Exception as e:
            return JsonResponse({"message": "", "error":"unknown failure"})
    else:
        return JsonResponse({"message":"method not Allowed"},status=403)