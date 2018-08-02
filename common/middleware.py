# coding: utf-8

import time

from django.core.cache import cache
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin


def simple_middleware(view_func):
    def middleware(request):
        print('exec ----> process_request')
        response = view_func(request)  # views 函数在这里执行
        print('exec ----> process_response')
        return response
    return middleware


class BlockMiddleware(MiddlewareMixin):
    '''
    -------------------
    1. 1533096000.00   t0
    2. 1533096000.37   t1
    3. 1533096000.95   t2
    -------------------
    4. 1533096000.99   now
    -------------------
    5. 1533096002.03
    6. 1533096003.03
    7. 1533096004.03
    8. 1533096005.03
    9. 1533096006.03
    '''
    def process_request(self, request):
        # 取出用户 IP，并设置相关 Key
        user_ip = request.META['REMOTE_ADDR']
        request_key = 'RequestTime-%s' % user_ip
        block_key = 'Blocker-%s' % user_ip

        # 检查用户是否被封禁
        if cache.get(block_key):
            return render(request, 'blockers.html')

        # 取出当前时间和历史访问时间
        now = time.time()
        t0, t1, t2 = cache.get(request_key, [0, 0, 0])

        if (now - t0) < 1:
            # 访问过频，封禁一天
            cache.set(block_key, 1, 86400)
            return render(request, 'blockers.html')
        else:
            # 更新访问时间
            cache.set(request_key, [t1, t2, now])
