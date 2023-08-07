"""User views"""
# pylint: skip-file

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer


# ...


class SignupView(APIView):
    """Signup view"""

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="User created successfully",
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid request",
            ),
        },
    )
    def post(self, request):
        # TODO - Add community geo id and update to profile table
        # TODO - Response - email, name, community_id
        """Signup view"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            try:
                # Check if user already exists
                User.objects.get(email=email)
                return Response(
                    {"error": "User with this email already exists."},
                    status=status.HTTP_409_CONFLICT,
                )
            except User.DoesNotExist:
                # Create a new user instance
                user = User(email=email)
                user.set_password(password)
                user.save()
                return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Login view"""

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "access_token": openapi.Schema(type=openapi.TYPE_STRING),
                        "refresh_token": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="Invalid credentials",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
        },
    )
    def post(self, request):
        """Login view"""
        email = request.data.get("email")
        password = request.data.get("password")

        # Retrieve the user based on the email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        # Verify the password
        if user.check_password(password):
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # TODO - User info - email, com id, name
            response_data = {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
            # TODO - Response - email, name, community_id
            # Return the tokens in the response
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class RefreshTokenView(APIView):
    """RefreshToken view"""
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "refresh_token": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Token refreshed successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "access_token": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid request",
            ),
        },
    )
    def post(self, request):
        """Refresh view"""
        refresh_token = request.data.get("refresh_token")

        # Attempt to verify and refresh the token
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            response_data = {
                "access_token": access_token,
            }

            # Return the new access token in the response
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception:
            # Handle invalid or expired refresh tokens
            return Response(
                {"error": "Invalid refresh token"},
                status=status.HTTP_400_BAD_REQUEST,
            )
