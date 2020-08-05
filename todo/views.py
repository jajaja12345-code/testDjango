
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
    listX = []

    form = PostForm()

    # print("posts in index")
    # print(posts)

    # for i in posts:
    # listX.append(i.getlist('body'))
    # print(i)
    # print(i.body)

    # イメージ
    # listAll = [["aa", "bb"], ["cc", "dd"]]

    # listX = ["aa", "bb"]
    context = {'posts': posts, 'form': form, 'listAll': listX}

    # context = {'posts': posts, 'form': form}

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
    # request.POST.update({'body': 'AAA'})

    ingS = ""
    ingRow = soup.find(id="ingredients_list").select(".ingredient_row")
# print(len(ingRow))
    for a in ingRow:
        try:
            # ingC = a.select_one(".ingredient_category").text
            ingS += "," + a.select_one(".ingredient_category").text + ":"

        except AttributeError as e:
            # print("Attributeerror occurs (in category)")
            #
            pass
        except:
            # print("some error occurs(in category)")
            pass
        else:
            pass

        try:
            ingS += "," + a.select_one(".name").text + "-"
        except AttributeError as e:
            # print("Attributeerror occurs (in name)")
            pass
            # continue
        except:
            # print("some error occurs(in name)")
            # continue
            pass
        else:
            # print(name)
            pass

        try:
            ingS += a.select_one(".ingredient_quantity.amount").text
        except AttributeError as e:
            # print("Attributeerror occurs (in quantity)")
            pass
            # continue
        except:
            # print("some error occurs(in quantity)")
            # continue
            pass
        else:
            # print(qAmount)
            pass

    request.POST['name'] = ingS
    # print(ingS)

    request.POST._mutable = False

    # 入力内容返却してくれる
    # print("request.POST: ")
    # print(request.POST)
    # print("request.POST['body']: " + request.POST['body'])
    # print("list size: " + str(len(request.POST)))  # OK
    # print("forで値が取り出せるかテスト")
    # for name in request.POST['body']:
    # print(name)  -> 出力AAA

    # print(request.POST.getlist('body'))
    # print(request.POST.getlist('body')[0])

    # for i in request.POST.getlist('body'):
    # print(i)

    # postformにlistフィールドはないけどこれで作れる
    # print(form)
    # form.list = request.POST.getlist('body')
    # form.list = "xxxxxxxxxxxxxx"

    # 基本的にquerydictは不変
    # request.POST['body'] = "change" ->怒られる

    # 変更後
    # form = PostForm(request.POST)
    # print("print form in create function")
    # print(form)

    form.save(commit=True)
    return HttpResponseRedirect(reverse('todo:index'))  # todo一覧にリダイレクトできる


def delete(request, id=None):  # urls.pyで設定したidがここに来る
    post = get_object_or_404(Post, pk=id)  # こいつについても後述
    post.delete()
    return HttpResponseRedirect(reverse('todo:index'))
