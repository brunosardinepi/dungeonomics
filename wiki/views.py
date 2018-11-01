from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from . import forms
from . import models
from . import utils


class ArticleDetail(View):
    def get(self, request, *args, **kwargs):
        articles = models.Article.objects.all().order_by('title')
        tags = models.Tag.objects.all()

        try:
            article = get_object_or_404(models.Article, pk=kwargs['pk'])
        except KeyError:
            if articles:
                article = articles[0]
            else:
                article = None

        if utils.is_wiki_admin(request.user):
            admin = True
        else:
            admin = False

        return render(request, 'wiki/article_detail.html', {
            'articles': articles,
            'tags': tags,
            'article': article,
            'admin': admin,
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

            # add the tags
            for tag in form.cleaned_data['tags']:
                article.tags.add(tag)

            # add admins
            utils.add_article_admins(article)
            article.admins.add(request.user)

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


class ArticleDelete(View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(models.Article, pk=kwargs['pk'])
        if utils.is_wiki_admin(request.user):
            article.delete()
            return redirect('wiki:article_detail')
        raise Http404
