from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .views import (
    home,
    post_detail,
    post_create,
    post_delete,
    post_update,
    my_articles,
    render_pdf_view,
    search,
    postComment,
    updateComment,
    deleteComment,
    UserPostListView,
)


urlpatterns = [
    path('', login_required(login_url=settings.LOGIN_URL)(home.as_view()), name='home'),
    path('user_posts/<str:username>', login_required(login_url=settings.LOGIN_URL)(UserPostListView.as_view()), name='user-posts'),
    path('post_create', post_create, name='post_create'),
    path('postComment', postComment, name='postComment'),
    path('updateComment/<slug:sno>', updateComment, name='updateComment'),
    path('deleteComment/<slug:sno>', deleteComment, name='deleteComment'),
    path('post_detail/<slug:slug>', post_detail, name='post_detail'),
    path('post_update/<slug:slug>', post_update, name='post_update'),
    path('post_delete/<slug:slug>', post_delete, name='post_delete'),
    path('my_articles', my_articles, name='my_articles'),
    path('search', search, name='search'),
    path('download/<slug:slug>', render_pdf_view, name='pdf'),
]