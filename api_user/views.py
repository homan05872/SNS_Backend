from django.shortcuts import render
from rest_framework import generics, authentication, permissions, viewsets, status
from api_user import serializers
from core.models import Profile, FriendRequest
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from core import custompermissions


class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


class FriendRequestViewSet(viewsets.ModelViewSet):
    '''友達申請view'''
    queryset = FriendRequest.objects.all()
    serializer_class = serializers.FriendRequestSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        '''askToかaskFromがログインユーザーであるものをクエリセットへ'''
        return self.queryset.filter(Q(askTo=self.request.user) | Q(askFrom=self.request.user))
      
    def perform_create(self, serializer):
        '''作成時、自動でaskFromがログインユーザーのものになる'''
        try:
            serializer.save(askFrom=self.request.user)
        except:
            raise ValidationError("User can have only unique request")

    def destory(self, request, *args, **kwargs):
        #Deleteを無効にするため、destoryメソッドをオーバーライド
        response = {'message': 'Delete is not allowed !'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
      
      
    def pertial_update(self, request, *args, **kwargs):
        #updateを無効にするため、destoryメソッドをオーバーライド
        response = {'message': 'Patch is not allowed !'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
  
  
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, custompermissions.ProfilePermission)
    
    def perform_create(self, serializer):
        serializer.save(userPro=self.request.user)
        

        
        
class MyProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return self.queryset.filter(userPro=self.request.user)
  