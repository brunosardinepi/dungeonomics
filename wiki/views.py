from django.shortcuts import get_object_or_404, render
from django.views import View

from . import models


class ArticleDetail(View):
    def get(self, request, *args, **kwargs):
        articles = models.Article.objects.all().order_by('title')
        try:
            article = get_object_or_404(models.Article, pk=kwargs['pk'])
        except KeyError:
            article = articles[0]
        return render(request, 'wiki/article_list.html', {
            'articles': articles,
            'article': article,
        })

class ArticleCreate(View):
    def get(self, request, *args, **kwargs):
        pass

class ArticleUpdate(View):
    def get(self, request, *args, **kwargs):
        pass
