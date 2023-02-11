import jwt
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from drf_yasg import openapi
from rest_framework import generics, status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsAuthenticated
from account.serializers import RegisterSerializer, LoginSerializer, AccountUpdateSerializer, \
    SetNewPasswordSerializer, ChangeNewPasswordSerializer, EmailVerificationSerializer
from account.models import Account


class AccountRegisterView(generics.GenericAPIView):
    # http://127.0.0.1:8000/account/api/register/
    serializer_class = RegisterSerializer

    # user create
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # user details or data
        return Response({'success': True, 'message': 'Activate url was sent your phone number'},
                        status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    # http://127.0.0.1:8000/api/account/v1/login/
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "message": f"Credentials are invalid {e}"},
                            status=status.HTTP_400_BAD_REQUEST)


class AccountRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    # http://127.0.0.1:8000/api/account/v1/retrieve-update/<id>/
    serializer_class = AccountUpdateSerializer
    queryset = Account.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        query = self.get_object()
        if query:
            serializer = self.get_serializer(query)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'message': 'query did not exist'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_202_ACCEPTED)
        return Response({'success': False, 'message': 'credentials is invalid'}, status=status.HTTP_404_NOT_FOUND)


# email-verification
class EmailVerificationAPIView(APIView):
    # http://127.0.0.1:8000/account/verify-email/?token={token}/
    serializer_class = EmailVerificationSerializer
    permission_classes = (AllowAny,)
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Verify email',
                                           type=openapi.TYPE_STRING)

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = Account.objects.get(id=payload['user_id'])
            if not user_id.is_active:
                user_id.is_active = True
                user_id.save()
            return Response({'success': True, 'message': 'Email successfully activated'},
                            status=status.HTTP_201_CREATED)
        except jwt.ExpiredSignatureError as e:
            return Response({'success': False, 'message': f'Verification expired | {e.args}'},
                            status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            return Response({'success': False, 'message': f'Invalid token | {e.args}'},
                            status=status.HTTP_400_BAD_REQUEST)


class SetPasswordConfirmAPIView(views.APIView):
    # http://127.0.0.1:8000/account/set-password-confirm/<uidb64>/<token>/
    permission_classes = (AllowAny,)

    def get(self, request, uidb64, token):
        try:
            _id = smart_str(urlsafe_base64_decode(uidb64))
            user = Account.objects.filter(id=_id).first()
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'success': False, 'message': 'Token is not valid, please try again'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)
        except DjangoUnicodeDecodeError as e:
            return Response({'success': False, 'message': f'DecodeError: {e.args}'},
                            status=status.HTTP_401_UNAUTHORIZED)
        return Response({'success': True, 'message': 'Successfully checked', 'uidb64': uidb64, 'token': token},
                        status=status.HTTP_200_OK)


class SetNewPasswordView(generics.UpdateAPIView):
    # http://127.0.0.1:8000/api/account/v1/set-password/
    serializer_class = SetNewPasswordSerializer
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({'success': True, 'message': 'Successfully set new password'}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'Credentials is invalid'}, status=status.HTTP_406_NOT_ACCEPTABLE)


# change password
class ChangePasswordCompletedView(generics.UpdateAPIView):
    # http://127.0.0.1:8000/account/change-password/
    queryset = Account.objects.all()
    serializer_class = ChangeNewPasswordSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            return Response({'success': True, 'message': 'Successfully set new password'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'{e}'})

    def put(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            return Response({'success': True, 'message': 'Successfully set new password'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'{e}'})


class AccountView(generics.RetrieveAPIView):
    # http://127.0.0.1:8000/api/account/v1/get-account/
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountUpdateSerializer

    def queryset(self, request, *args, **kwargs):
        user = request.user
        query = Account.objects.get(id=user.id)
        serializer = self.get_serializer(query)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
