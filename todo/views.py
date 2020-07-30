
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

    listX = ["aa", "bb"]
    context = {'posts': posts, 'form': form, 'listX': listX}

    # context = {'posts': posts, 'form': form}

    return render(request, 'todo/index.html', context)  # render関数については後述
    # index.htmlに関してはあとで作る


def create(request):
    form = PostForm(request.POST)
    print("request.POST: ")
    print(request.POST)

    request.POST._mutable = True
    url = request.POST['body']
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    ing = soup.find(id="ingredients")
    serv = ing.select_one(".servings_for.yield").text
    request.POST['body'] = serv
    request.POST.update({'body': 'AAA'})

    request.POST._mutable = False

    # 入力内容返却してくれる
    print("request.POST: ")
    print(request.POST)
    print("request.POST['body']: " + request.POST['body'])
    print("list size: " + str(len(request.POST)))  # OK
    print("forで値が取り出せるかテスト")
    for name in request.POST['body']:
        print(name)

    # 基本的にquerydictは不変
    # request.POST['body'] = "change"

    form.save(commit=True)
    return HttpResponseRedirect(reverse('todo:index'))  # todo一覧にリダイレクトできる


def delete(request, id=None):  # urls.pyで設定したidがここに来る
    post = get_object_or_404(Post, pk=id)  # こいつについても後述
    post.delete()
    return HttpResponseRedirect(reverse('todo:index'))
