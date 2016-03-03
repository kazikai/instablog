from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage

from .models import Post
from .models import Comment
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
def delete_comment(request, pk1, pk2):
    if request.method == 'GET':
        comment = get_object_or_404( Comment, pk=pk2 )
        comment.delete()
        return redirect( 'view_post', pk=pk1 );

def create_comment(request, post, pk):
    comment = Comment()
    comment.post = post
    comment.content = request.POST.get('comment')
    if comment.content is None:
        pass
    else:
        comment.save()
# 포스트 보기
def edit_post(request, pk):
    post = get_object_or_404( Post, pk=pk )
    categories = Category.objects.all()
    if request.method == 'GET':
        return render(request, 'edit_post.html', {
            'post': post,
            'categories': categories,
            })
    elif request.method == 'POST':
        post_edit = request.POST
        post.title = post_edit['title']
        post.content = post_edit['content']
        category = get_object_or_404(Category, pk=post_edit['category'])
        post.category = category
        post.save()
        return redirect('view_post', pk=post.pk)

# 포스트 보기
def view_post(request, pk):
    post = get_object_or_404( Post, pk=pk )
    if request.method == 'GET':
        return render(request, 'view_post.html', {
            'post': post,
            })
    elif request.method == 'POST':
        create_comment( request, post, pk )
        return redirect('view_post', pk=post.pk)

# 포스트 삭제
def delete_post(request, pk):
    post = get_object_or_404( Post, pk=pk )
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        post.delete()
        return redirect( '/' );
    return render(request, 'delete_post.html',{
        'post': pk
    })
# 포스트 만들기
def create_post(request):
    categories = Category.objects.all()
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
