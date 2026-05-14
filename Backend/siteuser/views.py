from django.shortcuts import render
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
 

# Create your views here.
class login(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        serializer = UserLoginSerializer(data=request.data)



        if serializer.is_valid(raise_exception=True):
            user = authenticate(username=username, password=password)

            if user is None:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)

            return Response({
                "user_id": user.id,
                "username": username,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                     }, status=status.HTTP_200_OK)



class user_register(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            user = serializer.save()
            token = RefreshToken.for_user(user)
            output_data = {
                "user_id": user.id,
                "username": user.username,
                "role": user.role,
                "access": str(token.access_token),
                "refresh": str(token),

            }
            return Response(output_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "role": user.role
        })