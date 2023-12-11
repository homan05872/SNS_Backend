# class ProfileViewSet(viewsets.ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = serializers.ProfileSerializer
#     authentication_classes = (authentication.TokenAuthentication)
#     permission_classes = (permissions.IsAuthenticated, custompermissions.ProfilePermission)
    
#     def perform_create(self, serializer):
#         serializer.save(userPro=self.request.user)
        
