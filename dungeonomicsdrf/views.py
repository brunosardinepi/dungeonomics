from django.contrib.auth.models import User
from dungeonomicsdrf import serializers
from rest_framework.response import Response
from rest_framework import generics


class SignupView(generics.GenericAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['password'] == request.data['passwordConfirm']:
                user = serializer.save()
                return Response(status=201)
        else:
            if serializer.errors:
                for error, messages in serializer.errors.items():
                    if error == "username":
                        for message in messages:
                            if str(message) == "A user with that username already exists.":
                                return Response(status=499)
                return Response(status=400)
