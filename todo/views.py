
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Post
from .forms import PostForm


# 7/27 change OK
from bs4 import BeautifulSoup
import requests

"""
url = "https://"
html = requests.get(url)
soup = BeautifulSoup(html.content, "html.parser")

ing = soup.find(id="ingredients")
serv = ing.select_one(".servings_for.yield").text
"""
#########


def index(request):
    posts = Post.objects.all()

    form = PostForm()
    """

    url = request.POST['body']
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    ing = soup.find(id="ingredients")
    serv = ing.select_one(".servings_for.yield").text
    """

    # context = {'posts': posts, 'form': form, 'serv': serv}
    context = {'posts': posts, 'form': form}

    return render(request, 'todo/index.html', context)  # render関数については後述
    # index.htmlに関してはあとで作る


def create(request):
    form = PostForm(request.POST)

    # 入力内容返却してくれる
    print(request.POST['body'])

    form.save(commit=True)
    return HttpResponseRedirect(reverse('todo:index'))  # todo一覧にリダイレクトできる


def delete(request, id=None):  # urls.pyで設定したidがここに来る
    post = get_object_or_404(Post, pk=id)  # こいつについても後述
    post.delete()
    return HttpResponseRedirect(reverse('todo:index'))
