
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Post
from .forms import PostForm


# 7/27 change OK
from bs4 import BeautifulSoup
import requests


# striptBlankとgetText合わせて取得した文を整形する
def stripBlank(text):
    lines = []
    for line in text.splitlines():
        lines.append(line.strip())
    rValue = "\n".join(line for line in lines if line)
    return rValue


def getText(a, csSelec):
    try:
        # ingC = a.select_one(".ingredient_category").text
        te = stripBlank(a.select_one(csSelec).text)

    except AttributeError as e:
        # print("Attributeerror occurs (in category)")
        if csSelec == ".ingredient_category":
            return None
        return ""
    except:
        # print("some error occurs(in category)")
        if csSelec == ".ingredient_category":
            return None
        return ""
    else:
        return te


def index(request):
    posts = Post.objects.all()
    listX = []

    form = PostForm()

    context = {'posts': posts, 'form': form, 'listAll': listX}

    return render(request, 'todo/index.html', context)  # render関数については後述
    # index.htmlに関してはあとで作る


def create(request):
    # 変更前
    form = PostForm(request.POST)
    # print("request.POST: ")
    # print(request.POST)

    request.POST._mutable = True
    url = request.POST['name']
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    ing = soup.find(id="ingredients")
    serv = ing.select_one(".servings_for.yield").text
    request.POST['url'] = serv

    ingS = ""
    ingRow = soup.find(id="ingredients_list").select(".ingredient_row")
    for a in ingRow:
        temp = getText(a, ".ingredient_category")
        if temp != None:
            ingS += ',' + temp + ':'
        ingS += ',' + getText(a, ".name") + "-"
        ingS += getText(a, ".ingredient_quantity.amount")

    request.POST['name'] = ingS
    # print(ingS)

    step = soup.find(id="steps").select(".step")
    stepText = ""
    for a in step:
        # print(stripBlank(a.select_one(".instruction").select_one(".step_text").text))
        stepText += ',' + stripBlank(a.select_one(
            ".instruction").select_one(".step_text").text)
    # print(stepText)
    stepText = "&&&&&&&&&&&"
    request.POST['url'] = stepText
    request.POST._mutable = False
    # print(request.POST['url'])

    form.save(commit=True)
    return HttpResponseRedirect(reverse('todo:index'))  # todo一覧にリダイレクトできる


def delete(request, id=None):  # urls.pyで設定したidがここに来る
    post = get_object_or_404(Post, pk=id)  # こいつについても後述
    post.delete()
    return HttpResponseRedirect(reverse('todo:index'))
