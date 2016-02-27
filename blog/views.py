from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage

from .models import Post
from .models import Category
# Create your views here.

def hello(request):
    return HttpResponse('hello world')

def hello_with_template(request):
    return render(request, 'hello.html')

def list_posts(request):
    per_page = 2
    current_page = request.GET.get('page', 1)

    #try:
        #request.GET 에 쿼리스트링 값이 저장된다.
        #current_page = request.GET.get('page', 1)
    #except ValueError:
    #    current_page = 1

    post_list = Post.objects.select_related().prefetch_related().all().order_by('-pk')

    page = Paginator( post_list, per_page )
    try:
        pg = page.page( current_page )
    except PageNotAnInteger:
        pg = page.page( 1 )
    except EmptyPage:
        pg = []

    #post_list = post_list[(current_page-1)*per_page:current_page*per_page]

    #start_offset = ( current_page - 1 ) * per_page
    #end_offset = ( current_page ) * per_page

    return render(request, 'list_posts.html', {
        #'posts': post_list,
        'posts': pg,
    })

def view_post(request, pk):
    post = get_object_or_404( Post, pk=pk )
    return render(request, 'view_post.html', {
        'post': post,
    })

def create_post(request):
    categories = Category.objects.all();
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        post = Post()
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.category = get_object_or_404( Category, pk=request.POST.get('category') )
        post.save()
        return redirect('view_post', pk=post.pk)
    return render(request, 'create_post.html',{
        'categories': categories,
        } )
