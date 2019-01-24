import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View

from .models import Webhook, WebhookAttribute


@method_decorator(login_required, name='dispatch')
class WebhookList(View):
    def get(self, request, *args, **kwargs):
        if request.user.email == 'gn9012@gmail.com':
            webhooks = Webhook.objects.all()
            return render(request, 'webhooks/webhook_list.html', {
                'webhooks': webhooks,
            })
        raise Http404

@method_decorator(login_required, name='dispatch')
class WebhookDetail(View):
    def get(self, request, *args, **kwargs):
        if request.user.email == 'gn9012@gmail.com':
            webhook = get_object_or_404(Webhook, pk=kwargs['pk'])
            webhook_attributes = WebhookAttribute.objects.filter(
                webhook=webhook).order_by('key')
            return render(request, 'webhooks/webhook_detail.html', {
                'webhook': webhook,
                'webhook_attributes': webhook_attributes,
            })
        raise Http404

@method_decorator(csrf_exempt, name='dispatch')
class SNS_Webhook(View):
    def post(self, request, *args, **kwargs):
        webhook = Webhook.objects.create(provider="AWS")
        message = json.loads(request.body.decode('utf-8'))
        for key, value in message.items():
            webhook_key = WebhookAttribute.objects.create(
                webhook=webhook,
                key=key,
                value=value,
            )
        return HttpResponse(status=200)
