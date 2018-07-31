# coding: utf-8

from django.core.cache import cache


def page_cache(view_func):
    def wrapper(request):
        key = 'PageCache-%s-%s' % (request.session_key, request.get_full_path())
        response = cache.get(key)
        if response is None:
            response = view_func(request)
            cache.set(key, response)
        return response
    return wrapper
