from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from account.models import Account


# Register
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    password2 = serializers.CharField(min_length=6, max_length=68, write_only=True)
    avatar = serializers.ImageField()

    class Meta:
        model = Account
        fields = (
            'full_name',
            'phone_number',
            'avatar',
            'password',
            'password2'
        )

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError({'success': False, 'message': 'Password did not match, please try again'})
        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        return Account.objects.create_user(**validated_data)


# Login
class LoginSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=16, required=True)
    full_name = serializers.CharField(max_length=223, read_only=True)
    email = serializers.EmailField(read_only=True)
    password = serializers.CharField(max_length=68, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)

    def get_token(self, obj):
        phone_number = obj.get('phone_number')
        token = Account.objects.get(phone_number=phone_number).token
        return token

    class Meta:
        model = Account
        fields = (
            'phone_number',
            'full_name',
            'email',
            'token',
            'password'
        )

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')
        user: Account = authenticate(phone_number=phone_number, password=password)
        if not user:
            raise AuthenticationFailed({
                'message': 'Phone or password is not correct'
            })
        data = {
            'phone_number': user.phone_number,
            'full_name': user.full_name,
            'email': user.email
        }
        return data


# email-verification
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = Account
        fields = ('token',)


# Account page
class AccountUpdateSerializer(serializers.ModelSerializer):
    gender_display = serializers.SerializerMethodField()

    @staticmethod
    def get_gender_display(obj):
        return obj.get_gender_display()

    class Meta:
        model = Account
        fields = (
            'id', 'full_name', 'avatar', 'phone_number', 'email', 'town_city', 'date_birth', 'gender', 'gender_display')


# Set-password
class SetNewPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=64, write_only=True)
    password2 = serializers.CharField(min_length=6, max_length=64, write_only=True)

    class Meta:
        model = Account
        fields = ('password', 'password2')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        request = self.context['request']
        user = request.user
        current_password = user.password
        if password != password2:
            raise serializers.ValidationError({'success': False, 'message': 'Password did not match, '
                                                                            'please try again new'})
        if check_password(password, current_password):
            raise serializers.ValidationError(
                {'success': False, 'message': 'New password should not similar to current password'})
        user.set_password(password)
        user.save()
        return attrs


# Account change password
class ChangeNewPasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(min_length=3, max_length=64, write_only=True)
    password = serializers.CharField(min_length=3, max_length=64, write_only=True)
    password2 = serializers.CharField(min_length=3, max_length=64, write_only=True)

    class Meta:
        model = Account
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        request = self.context.get('request')
        user = request.user
        if not user.check_password(old_password):
            raise serializers.ValidationError(
                {'success': False, 'message': 'Old password did not match, please try again new'})
        if password != password2:
            raise serializers.ValidationError(
                {'success': False, 'message': 'Password did not match, please try again new'})
        user.set_password(password)
        user.save()
        return attrs


# Account user data
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("id", "full_name", "phone_number", "email", "town_city")
