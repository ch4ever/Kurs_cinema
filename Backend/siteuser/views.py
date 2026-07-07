from drf_spectacular.utils import extend_schema
from .serializers import *
from rest_framework import permissions
from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .services import auth_user, create_auth_tokens

 

class login(APIView):

    @extend_schema(
        summary="Login",
        description="Login with username and password",
        tags=["SiteUser"],
        request=UserLoginSerializer,
        responses={
            status.HTTP_200_OK: SuccessAuthLoginSerializer(),
            status.HTTP_401_UNAUTHORIZED: None,
        },
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            data = auth_user(username,password)
            if data is None:
                return Response({"detail":"Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

            output_serializer = SuccessAuthLoginSerializer(data)

            return Response(output_serializer.data, status=status.HTTP_200_OK)



class user_register(APIView):
    permission_classes = (permissions.AllowAny,)

    @extend_schema(
        summary="Register",
        description="Register a new user",
        tags=["SiteUser"],
        request=UserRegisterSerializer,
        responses=SuccessAuthLoginSerializer,
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            user = serializer.save()
            data = create_auth_tokens(user)
            output_serializer = SuccessAuthLoginSerializer(data)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @extend_schema(
        summary="Getme",
        description="Get ur basic data",
        tags=["SiteUser"],
        responses={
            status.HTTP_200_OK: UserSerializer,
        }
    )
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
