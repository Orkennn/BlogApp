from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import CommentForm

# Create your views here.
from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, DetailView
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'


class DetailPostListView(DetailView):
    model = Post
    template_name = 'detail_post_view.html'


def about_page(request):
    return render(request, 'about.html')


def contacts_page(request):
    return render(request, 'contacts.html')


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'detail_post_view.html', {'post': post, 'form': form})