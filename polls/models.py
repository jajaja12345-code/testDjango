import datetime  # ここを追加

from django.db import models
from django.utils import timezone  # ここを追加


class Question(models.Model):
    question_text = models.CharField(max_length=200)  # 質問文
    pub_date = models.DateTimeField('date published')  # 公開日

    def __str__(self):  # ここを追加
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE)  # 質問文の読み込み
    choice_text = models.CharField(max_length=200)  # 質問に対する選択肢
    votes = models.IntegerField(default=0)  # 投票数

    def __str__(self):  # ここを追加
        return self.choice_text
