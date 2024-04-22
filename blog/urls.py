from django.urls import path

from . import views
from .views import PostListView, DetailPostListView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('<int:pk>/', DetailPostListView.as_view(), name='post-detail'),
    path('post/<int:pk>/comment/', views.post_detail, name='add_comment_to_post'),
    path('about/', views.about_page, name='about'),
    path('contacts/', views.contacts_page, name='contacts'),

]
