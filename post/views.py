from math import ceil

from django.core.cache import cache
from django.shortcuts import render, redirect

from post.models import Post


def post_list(request):
    page = int(request.GET.get('page', 1))  # 当前页码
    total = Post.objects.count()            # 帖子总数
    per_page = 10                           # 每页帖子数
    pages = ceil(total / per_page)          # 总页数

    start = (page - 1) * per_page
    end = start + per_page

    posts = Post.objects.all().order_by('-id')[start:end]  # 惰性加载 懒加载
    return render(request, 'post_list.html',
                  {'posts': posts, 'pages': range(pages)})


def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(title=title, content=content)
        return redirect('/post/read/?post_id=%s' % post.id)
    return render(request, 'create_post.html')


def edit_post(request):
    if request.method == 'POST':
        post_id = int(request.POST.get('post_id'))
        post = Post.objects.get(id=post_id)
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()

        # 更新缓存
        key = 'Post-%s' % post_id
        cache.set(key, post)  # 存入缓存
        return redirect('/post/read/?post_id=%s' % post.id)
    else:
        post_id = request.GET.get('post_id')
        post = Post.objects.get(id=post_id)
        return render(request, 'edit_post.html', {'post': post})


def read_post(request):
    post_id = int(request.GET.get('post_id'))
    key = 'Post-%s' % post_id
    # 先从缓存获取
    post = cache.get(key)
    print('Get from cache:', post)

    if post is None:  # 检查缓存数据
        # 如果不存在，直接从数据库获取
        post = Post.objects.get(id=post_id)
        print('Get from DB:', post)
        cache.set(key, post)  # 存入缓存
        print('Set to cache')
    return render(request, 'read_post.html', {'post': post})


def search(request):
    keyword = request.POST.get('keyword')
    posts = Post.objects.filter(content__contains=keyword)
    return render(request, 'search.html', {'posts': posts})
