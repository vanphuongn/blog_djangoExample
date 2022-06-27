from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import EmailPostForm
# Create your views here.

def post_list(request):
    # posts = Post.published.all()
    object_list = Post.objects.all()
    paginator = Paginator(object_list,2)
    pageNumber = request.GET.get('page')

    try:
        posts = paginator.page(pageNumber)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post/index.html',{"posts":posts,
                                                  'page':pageNumber
                                                  })

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk = post_id)
    return render(request, "blog/post/detail.html",{"post": post})

def post_share(request, post_id):
    post = get_object_or_404(Post,pk = post_id, status = 'published')
    if request.method =="POST":
        #form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #send email
    else:
        form = EmailPostForm()
    context = {
        "post":post,
        "form":form
    }
    return render(request, "blog/post/share.html",context)