
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

    a = ""
    b = ""

    if(a in url):
        print("title:" + stripBlank(soup.find(
            id="recipe-title").select_one(".recipe-title.fn.clearfix").get_text()))
        ing = soup.find(id="ingredients")
        serv = ing.select_one(".servings_for.yield").text
        request.POST['url'] = serv
        print("servings_for yield:" + stripBlank(serv))
        ingS = ""
        ingRow = soup.find(id="ingredients_list").select(".ingredient_row")
        for a in ingRow:
            temp = getText(a, ".ingredient_category")
            if temp != None:
                ingS += temp + '\n'
            ingS += getText(a, ".name") + ":"
            ingS += getText(a, ".ingredient_quantity.amount") + '\n'
        print("材料:")
        print(ingS)
        print("step:")
        ingStep = soup.find(id="steps").select(".step")
        stepText = ""
        for a in ingStep:
            print(stripBlank(a.select_one(
                ".instruction").select_one(".step_text").text))
            stepText += ',' + stripBlank(a.select_one(
                ".instruction").select_one(".step_text").text)

    elif(b in url):
        print("title:" + stripBlank(soup.select_one(".title-wrapper").get_text()))
        ingS = ""
        ingList = soup.select_one(".ingredient-list").find_all("li")
        for a in ingList:
            tempS = getText(a, ".ingredient-name")
            if(tempS == ""):
                ingS += getText(a, ".ingredient-title") + ":"
            else:
                ingS += tempS + ":"
            ingS += getText(a, ".ingredient-quantity-amount") + '\n'
        print("材料:")
        print(ingS)
        print("step:")
        ingStep = soup.select_one(
            ".instruction-list").select(".instruction-list-item")
        stepText = ""
        for a in ingStep:
            print(stripBlank(a.select_one(".content").text))
            stepText += ',' + stripBlank(a.select_one(".content").text)

    else:
        print("そのurlに対応する処理はありません")
        ingS = "そのurlに対応する"
        stepText = "処理はありません"

    request.POST['name'] = ingS
    request.POST['url'] = stepText
    request.POST._mutable = False

    form.save(commit=True)
    return HttpResponseRedirect(reverse('todo:index'))  # todo一覧にリダイレクトできる


def delete(request, id=None):  # urls.pyで設定したidがここに来る
    post = get_object_or_404(Post, pk=id)  # こいつについても後述
    post.delete()
    return HttpResponseRedirect(reverse('todo:index'))
