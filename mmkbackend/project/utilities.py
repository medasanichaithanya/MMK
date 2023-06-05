from django.core.cache import cache
from datetime import  timedelta
import json
import base64
from project.models import *

def check_rate_limit(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        from_param = body['from'] if body['from']  else  ''
        cache_key = f"{from_param}_request_count"
        request_count = cache.get(cache_key, 0)
        if request_count >= 3:
            return False," " 
        
        cache.set(cache_key, request_count + 1, int(timedelta(days=1).total_seconds()))

    return True,from_param


def auth_check(request):
    if request.method == 'POST':
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2 and auth[0].lower() == 'basic':
            username, password = base64.b64decode(auth[1]).decode().split(':')
            if username and password:
                check_user = Account.objects.filter(username=username,auth_id=password)
                if check_user:
                    return True
                else:
                    False   
            else:
                return False
        else:
            return False
    return False

def validate_toparam(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        to_param = body['to'] if body['to']  else  ''
        if 6<=len(to_param)<=16 :
            check_to_param = Phone_number.objects.filter(number=int(to_param))
            if check_to_param:
                   return True,str("valid")
            else:
                return False,str("to param is not found")
        else:
            return False,str("to param is invalid")
    else:
        return False,""
    
def validate_fromparam(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        from_param = body['from'] if body['from']  else  ''
        if 6<=len(from_param)<=16 :
            check_to_param = Phone_number.objects.filter(number=int(from_param))
            if check_to_param:
                   return True,str("valid")
            else:
                return False,str("from param is not found")
        else:
            return False,str("from param is invalid")
    else:
        return False,""

