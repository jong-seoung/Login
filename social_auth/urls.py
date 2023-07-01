from django.urls import path
from .kakao_login import KakaoLoginView, KakaoCallbackView, KakaoLogin

urlpatterns = [
    path('kakao/login/', KakaoLoginView.as_view(), name='kakao-login'),
    path('kakao/callback/', KakaoCallbackView.as_view(), name='kakao-callback'),
    path('kakao/login/finish/', KakaoLogin.as_view(), name='kakao')
]
