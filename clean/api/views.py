from datetime import datetime, timedelta

import pytz
from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated

from blog.models import Post
from .serializers import PostSerializer


class ExpireTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('invalid token')

        if not token.user.is_active:
            raise AuthenticationFailed('user inactive or deleted')

        utc_now = datetime.utcnow()
        utc_now.replace(tzinfo=pytz.utc)


        if token.created < utc_now - timedelta(minutes=2):
            raise AuthenticationFailed('token has expired')

        return token.user, token


class ObtainExpireAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.validated_data.get('user'))

            if not created:
                token.created = datetime.utcnow()
                token.save()

            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostViewSet(ModelViewSet):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer
    authentication_classes = [ExpireTokenAuthentication]
    permission_classes = [IsAuthenticated]


obtain_expire_auth_token = ObtainExpireAuthToken.as_view()
