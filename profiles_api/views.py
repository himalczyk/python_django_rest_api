from tokenize import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions


class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer
    
    def get(self, request, format=None):
        """Retrusn a list of APIView freatures"""
        
        an_apiview = [
            'Users HTTP methods as functino (get, post, patch, put, delete',
            'Is similar to a traditional django view',
            'Gives you the most control over the app logic',
            'Is mapped manually to URLs',
        ]
        
        return Response({'message' : 'hello', 'an_apiview': an_apiview})
        
    def post(self, request):
        """Create a Hello message with our name"""
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():    
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                )
            
    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({'method': 'PUT'})
    
    def patch(self, request, pk=None):
        """Handle a partial update of an object"""
        return Response({'method': 'PATCH'})
    
    def delete(self, request, pk=None):
        """Handle deleting of an object"""
        return Response({'method': 'DELETE'})
    
class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = serializers.HelloSerializer
    
    def list(self, request):
        """Return a Hello message"""
        a_viewset = [
            'Users actions: list, create, retrieve, update, partial_update',
            'Automatically maps to URLs using ROuters',
            'Provides more functionality with less code'
        ]
        
        return Response({'message':'Hello', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
            
    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'http_method': 'GET'})
    
    def update(self, request, pk=None):
        """Handle updating of an object"""
        return Response({'http_method': 'PUT'})
    
    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http_method': 'PATCH'})
    
    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({'http_method': 'DELETE'})
    
class ProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email')
    
class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    
class UserProfileFeedItemViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    
    # user token auth to auth requests, comma at the end to pass it in as a tuple
    authentication_classes = (TokenAuthentication,)
    # set a serializer class created in serializers for the view
    serializer_class = serializers.ProfileFeedItemSerializer
    # assign a queryset that is going to be managed by the viewset
    queryset = models.ProfileFeedItem.objects.all()
    # user authentication or read only requests allowed
    permission_classes = (
        permissions.UpdateOwnStatus,
        # IsAuthenticatedOrReadOnly,
        # restrict viewing to logged in users only
        IsAuthenticated
    )
    
    # build in django feature allows overwriting/customizing behavior. gets called by every https post
    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        # request is an object that gets passed to all viewsets every time a request is made, contains all details about the request being made to the viewset
        # if user is authenticated request has the user field
        serializer.save(user_profile=self.request.user)
        
    