from django.urls import path
from .kakao_login import KakaoLoginView, KakaoCallbackView, KakaoLogin
from .github_login import GithubLoginView, GithubCallbackView, GithubLogin

urlpatterns = [
    path('kakao/login/', KakaoLoginView.as_view(), name='kakao-login'),
    path('kakao/callback/', KakaoCallbackView.as_view(), name='kakao-callback'),
    path('kakao/login/finish/', KakaoLogin.as_view(), name='kakao'),

    path("github/login/", GithubLoginView.as_view(), name="github_login"),
    path("github/callback/", GithubCallbackView.as_view(), name="github_callback"),
    path("github/login/finish/", GithubLogin.as_view(), name="github_login_to_django"),
]
