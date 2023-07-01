from django.shortcuts import redirect
from accounts.models import User
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from allauth.socialaccount.models import SocialAccount
from rest_framework import status
from django.conf import settings
from dj_rest_auth.registration.views import SocialLoginView
from django.http import JsonResponse
import requests
from .serializers import TokenResponseSerializer
from rest_framework.response import Response
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client


class Constants:
    BASE_URL = "http://127.0.0.1:8000/"

    REST_API_KEY = getattr(settings, "KAKAO_REST_API_KEY")
    KAKAO_CALLBACK_URI = f"{BASE_URL}api/v1/user/kakao/callback/"


class KakaoLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={Constants.REST_API_KEY}"
            f"&redirect_uri={Constants.KAKAO_CALLBACK_URI}&response_type=code"
        )


class KakaoCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        BASE_URL = Constants.BASE_URL
        REST_API_KEY = Constants.REST_API_KEY
        KAKAO_CALLBACK_URI = Constants.KAKAO_CALLBACK_URI
        code = request.GET.get("code")
        """
            Access Token Request
        """
        token_req = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}"
            f"&redirect_uri={KAKAO_CALLBACK_URI}&code={code}"
        )
        token_req_json = token_req.json()
        error = token_req_json.get("error")
        if error is not None:
            if token_req_json.get("error") == "invalid_request":
                return redirect(f"{BASE_URL}api/v1/user/kakao/login")
            return JsonResponse(token_req_json)
        access_token = token_req_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account")
        email = kakao_account.get("email")
        try:
            user = User.objects.get(email=email)
            social_user = SocialAccount.objects.get(user=user)
            if social_user is None:
                return JsonResponse(
                    {"err_msg": "email exists but not social user"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if social_user.provider != "kakao":
                return JsonResponse(
                    {"err_msg": "no matching social type"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            data = {"access_token": access_token, "code": code}
            accept = requests.post(
                f"{BASE_URL}api/v1/user/kakao/login/finish/", data=data
            )
            accept_status = accept.status_code
            if accept_status != 200:
                return JsonResponse(
                    {"err_msg": "failed to signin"}, status=accept_status
                )
            serializer = TokenResponseSerializer(user)
            data = serializer.to_representation(serializer)
            res = Response(
                data,
                status=status.HTTP_200_OK,
            )
            return res
        except User.DoesNotExist:
            data = {"access_token": access_token, "code": code}
            accept = requests.post(
                f"{BASE_URL}api/v1/user/kakao/login/finish/", data=data
            )
            accept_status = accept.status_code
            if accept_status != 200:
                return JsonResponse(
                    {"err_msg": "failed to signup"}, status=accept_status
                )
            user = User.objects.get(email=email)
            serializer = TokenResponseSerializer(user)
            data = serializer.to_representation(serializer)
            res = Response(
                data,
                status=status.HTTP_200_OK,
            )
            return res


class KakaoLogin(SocialLoginView):
    permission_classes = [AllowAny]

    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = Constants.KAKAO_CALLBACK_URI
