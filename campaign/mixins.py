from django.contrib import messages

class SuccessMessageMixin:
    success_message = ""

    def get_success_message(self):
        return self.success_message

    def form_valid(self, form):
        messages.success(self.request, get_success_message(self))
        return super().form_valid(form)