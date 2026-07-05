from dataclasses import dataclass

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import defaultUser


@dataclass(frozen=True)
class Tokens:
    access: str
    refresh: str

@dataclass(frozen=True)
class LoginResult:
    user: defaultUser
    tokens: Tokens


def create_auth_tokens(user: defaultUser) -> LoginResult:
    refresh = RefreshToken.for_user(user)

    return LoginResult(
        user=user,
        tokens=Tokens(
            access=str(refresh.access_token),
            refresh=str(refresh),
        )
    )


def auth_user(username: str, password: str) -> LoginResult | None:
    user = authenticate(username=username,password=password)

    if user is None:
        return None

    return create_auth_tokens(user)

        