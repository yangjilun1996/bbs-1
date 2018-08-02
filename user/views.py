from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password

from user.models import User
from user.forms import RegisterForm
from user.helper import get_wb_access_token
from user.helper import get_wb_user_show
from user.helper import login_required


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)
            user.save()

            # 设置用户登录状态
            request.session['uid'] = user.id
            request.session['nickname'] = user.nickname
            request.session['avatar'] = user.avatar
            return redirect('/user/info/')
        else:
            return render(request, 'register.html', {'error': form.errors})
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')

        try:
            user = User.objects.get(nickname=nickname)
        except User.DoesNotExist:
            return render(request, 'login.html',
                          {'error': '用户不存在', 'auth_url': settings.WB_AUTH_URL})

        if check_password(password, user.password):
            # 设置用户登录状态
            request.session['uid'] = user.id
            request.session['nickname'] = user.nickname
            request.session['avatar'] = user.avatar
            return redirect('/user/info/')
        else:
            return render(request, 'login.html',
                          {'error': '密码错误', 'auth_url': settings.WB_AUTH_URL})
    return render(request, 'login.html', {'auth_url': settings.WB_AUTH_URL})


def logout(request):
    request.session.flush()
    return redirect('/user/login/')


@login_required
def user_info(request):
    uid = request.session['uid']
    user = User.objects.get(id=uid)
    return render(request, 'user_info.html', {'user': user})


def wb_callback(request):
    code = request.GET.get('code')

    # 获取 access_token
    result = get_wb_access_token(code)
    if 'error' in result:
        return render(request, 'login.html',
                      {'error': result['error'], 'auth_url': settings.WB_AUTH_URL})
    uid = result['uid']
    access_token = result['access_token']

    # 获取个人信息
    result = get_wb_user_show(access_token, uid)
    if 'error' in result:
        return render(request, 'login.html',
                      {'error': result['error'], 'auth_url': settings.WB_AUTH_URL})

    user, created = User.objects.get_or_create(nickname=result['screen_name'])
    if created:
        user.plt_icon = result['avatar_large']
        user.save()

    # 设置用户登录状态
    request.session['uid'] = user.id
    request.session['nickname'] = user.nickname
    request.session['avatar'] = user.avatar
    return redirect('/user/info/')
