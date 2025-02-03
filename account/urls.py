from django.urls import path
from .views import (
    AccountRegisterView, LoginView, AccountRetrieveUpdateView,
    SetPasswordConfirmAPIView, SetNewPasswordView, ChangePasswordCompletedView,
    EmailVerificationAPIView, AccountUserMeView, AccountUsersView,
)

urlpatterns = [
    path('register/', AccountRegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/<int:pk>/', AccountRetrieveUpdateView.as_view()),
    path('verify-email/', EmailVerificationAPIView.as_view()),
    path('set-password-confirm/<str:uidb64>/<str:token>/', SetPasswordConfirmAPIView.as_view()),
    path('set-password-comfirmed/', SetNewPasswordView.as_view()),
    path('change-password-comfirmed/', ChangePasswordCompletedView.as_view()),
    path('me/', AccountUserMeView.as_view()),
    path('profiles/', AccountUsersView.as_view()),
]
