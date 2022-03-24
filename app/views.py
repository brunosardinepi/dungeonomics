from app import models, serializers
from datetime import timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View
from dungeonomicsdrf import environ
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class PasswordResetAction(generics.UpdateAPIView):
    lookup_field = "uuid"
    queryset = models.PasswordReset.objects.all()
    serializer_class = serializers.PasswordResetSerializer
    permission_classes = []

    def perform_update(self, serializer):
        # Check that the POSTed passwords match, then update the user's password.
        password_reset = serializer.save()
        if (
            password_reset.email == self.request.data['username'] and
            str(password_reset.uuid) == self.request.data['passwordReset'] and
            self.request.data['password'] == self.request.data['passwordConfirm']
        ):
            user = User.objects.get(email=password_reset.email)
            user.set_password(self.request.data['password'])
            user.save()
            password_reset.is_completed = True
            password_reset.save()

class PasswordResetRequest(generics.CreateAPIView):
    queryset = models.PasswordReset.objects.all()
    serializer_class = serializers.PasswordResetSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)

        # Check that a user exists for the requested email.
        try:
            user = User.objects.get(email=serializer.data['email'])
        except User.DoesNotExist as error:
            print("error", error)
            return error

        # Check that the user's last password reset was at least 5 minutes ago.
        password_resets = models.PasswordReset.objects.filter(
            email=user.email,
            is_completed=False,
        )
        five_minutes_ago = timezone.now() - timedelta(minutes=5)

        if (
            (
                password_resets.count() > 0 and
                password_resets.first().created_at <= five_minutes_ago
            )
            or password_resets.count() == 0
        ):
            # Create password reset.
            password_reset = models.PasswordReset.objects.create(email=user.email)

            # Send email with password reset URL.
            send_mail(
                subject="Password reset",
                message=(
                    f"This email was sent to you because someone requested "
                    f"a password reset for this email address. Go here and use your "
                    f"password reset code to reset your password:\n\n"
                    f"{environ.secrets['protocol']}://{environ.secrets['domain']}/password-reset/action\n"
                    f"Password reset code: {password_reset.uuid}"
                ),
                from_email=environ.secrets['email_from'],
                recipient_list=[user.email],
                fail_silently=False,
            )

            return Response({}, status=201, headers=headers)

        return Response({}, status=400, headers=headers)
