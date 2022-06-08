from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import ListView
from django.template.loader import get_template
from xhtml2pdf import pisa

from django.contrib.auth.models import User
from .models import Post, Comment
from .forms import PostForm
from articles.templatetags import extras


class home(ListView):
    model = Post
    template_name = 'articles/home.html'
    context_object_name = 'articles'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.all()


class UserPostListView(ListView):
    model = Post
    template_name = 'articles/user_posts.html'
    context_object_name = 'articles'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-published_at')


@login_required(login_url=settings.LOGIN_URL)
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/post_create.html', context)


@login_required(login_url=settings.LOGIN_URL)
def post_detail(request, slug):
    article = Post.objects.filter(slug=slug).first()
    comments = Comment.objects.filter(post=article)

    context = {
        'article': article,
        'comments': comments,
    }

    return render(request, 'articles/post_detail.html', context)


@login_required(login_url=settings.LOGIN_URL)
def post_update(request, slug):
    article = Post.objects.get(slug=slug)
    if article.author == request.user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=article)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                messages.success(request, 'Article Updated')
                return redirect('post_detail', slug=post.slug)
        else:
            form = PostForm(instance=article)
        context = {
            'form': form,
        }
        return render(request, 'articles/post_update.html', context)
    else:
        return redirect('/')


@login_required(login_url=settings.LOGIN_URL)
def post_delete(request, slug):
    article = Post.objects.get(slug=slug)
    if article.author == request.user:
        if request.method == 'POST':
            article.delete()
            return redirect('/')
        return render(request, 'articles/post_delete.html')
    else:
        return redirect('/')


@login_required(login_url=settings.LOGIN_URL)
def my_articles(request):
    article_list = Post.objects.all().filter(author=request.user)
    paginator = Paginator(article_list, 3)

    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    context = {
        'articles': articles,
    }
    return render(request, 'articles/my_articles.html', context)


@login_required(login_url=settings.LOGIN_URL)
def postComment(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        user = request.user
        slug = request.POST.get('slug')
        post = Post.objects.get(slug=slug)

        comment = Comment(content=content, user=user, post=post)
        messages.success(request, 'Comment Posted')
        comment.save()

        return redirect('post_detail', slug=post.slug)


@login_required(login_url=settings.LOGIN_URL)
def updateComment(request, sno):
    comment = Comment.objects.get(sno=sno)
    if comment.user == request.user:
        if request.method == 'POST':
            content = request.POST.get('content')
            post = comment.post
            comment.content = content
            messages.success(request, 'Comment Updated')
            comment.save()

            return redirect('post_detail', slug=post.slug)
        return render(request, 'articles/updateComment.html', {'comment': comment})
    else:
        return redirect('/')


@login_required(login_url=settings.LOGIN_URL)
def deleteComment(request, sno):
    comment = Comment.objects.get(sno=sno)
    slug = comment.post.slug
    if comment.user == request.user:
        if request.method == 'POST':
            comment.delete()
            return redirect('post_detail', slug=slug)
        return render(request, 'articles/deleteComment.html')
    else:
        return redirect('/')


@login_required(login_url=settings.LOGIN_URL)
def search(request):
    context = {}

    q = ''
    if request.GET:
        q = request.GET.get('query', '')
        context['q'] = str(q)

    if len(q) > 1 and len(q) < 78:
        articles = Post.objects.filter(Q(title__icontains=q) | Q(description__icontains=q))

        page = request.GET.get('page', 1)
        articles_paginator = Paginator(articles, 3)
        try:
            articles = articles_paginator.page(page)
        except PageNotAnInteger:
            articles = articles_paginator.page(3)
        except EmptyPage:
            articles = articles_paginator.page(articles_paginator.num_pages)
    else:
        articles = Post.objects.none()

    context['articles'] = articles
    return render(request, 'articles/search.html', context)


@login_required(login_url=settings.LOGIN_URL)
def render_pdf_view(request, slug):
    article = Post.objects.get(slug=slug)
    template_path = 'articles/pdf.html'
    context = {'article': article}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # if download:
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # if display:
    response['Content-Disposition'] = f'filename="{article}.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response