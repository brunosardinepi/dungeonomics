from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.views import View

from . import forms
from . import models
from . import utils


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
        if utils.is_wiki_admin(request.user):
            form = forms.ArticleForm()
            return render(request, 'wiki/article_form.html', {
                'form': form,
            })
        raise Http404

    def post(self, request, *args, **kwargs):
        form = forms.ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.creator = request.user
            article.save()
            utils.add_article_admins(article)
            messages.add_message(request, messages.SUCCESS, "Article created")
            return HttpResponseRedirect(article.get_absolute_url())
        raise Http404


class ArticleUpdate(View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(models.Article, pk=kwargs['pk'])
        if utils.is_article_admin(request.user, article):
            form = forms.ArticleForm(instance=article)
            return render(request, 'wiki/article_form.html', {
                'article': article,
                'form': form,
            })
        raise Http404

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(models.Article, pk=kwargs['pk'])
        form = forms.ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Updated article")
            return HttpResponseRedirect(article.get_absolute_url())
        raise Http404
