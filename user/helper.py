import requests
from django.shortcuts import render, redirect
from django.conf import settings

from user.models import User


def get_wb_access_token(code):
    '''获取微博 access_token'''
    args = settings.WB_ACCESS_TOKEN_ARGS.copy()
    args['code'] = code
    response = requests.post(settings.WB_ACCESS_TOKEN_API, data=args)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'Weibo server error'}


def get_wb_user_show(access_token, uid):
    '''获取微博个人信息'''
    args = settings.WB_USER_SHOW_ARGS.copy()
    args['access_token'] = access_token
    args['uid'] = uid
    response = requests.get(settings.WB_USER_SHOW_API, params=args)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'Weibo server error'}


def login_required(view_func):
    def wrapper(request):
        uid = request.session.get('uid')
        if uid is None:
            return redirect('/user/login/')
        else:
            return view_func(request)
    return wrapper


def check_perm(perm_name):
    def deco(view_func):
        def wrapper(request):
            uid = request.session['uid']
            user = User.objects.get(id=uid)

            if user.has_perm(perm_name):
                return view_func(request)
            else:
                return render(request, 'blockers.html')
        return wrapper
    return deco
