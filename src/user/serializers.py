from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from src.custom_lib.functions import current_user
from src.user_group.models import UserGroup

User = get_user_model()

class  GetGroupSerializer(serializers.ModelSerializer):
      class Meta:
        model = UserGroup
        exclude = ['active','permissions','created_date_ad','created_date_bs','created_by']


class UserListSerializer(serializers.ModelSerializer):
    '''
    serializer for get user list
    '''
    user_group_name = serializers.ReadOnlyField(
        source='group.name', allow_null=True)
    # user_type_display = serializers.ReadOnlyField(source="get_user_type_display", allow_null=True)
    class Meta:
        model = User
        exclude = ['password','groups','user_type']

    def to_representation(self, instance):
        '''
        Method for add extra key value pair
        '''
        my_fields = {'birth_date', 'created_by', 'user_group_name'}
        data = super().to_representation(instance)
        if data['group']  is not None:
            group = UserGroup.objects.get(id=data["group"])
            group_data = GetGroupSerializer(group)
            data['group'] =  group_data.data
        for field in my_fields:
            try:
                if not data[field]:
                    data[field] = ""
            except KeyError:
                pass
        return data


class RegisterUserSerializer(serializers.ModelSerializer):
    '''
    serializer used to register user to the system
    '''
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    user_name = serializers.CharField(
        min_length=4, max_length=50, required=True, allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, min_length=6,
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('user_name', 'password', 'confirm_password', 'email',
                  'first_name', 'last_name', 'middle_name', 'active', 'gender', 'birth_date',
                  'address', 'mobile_no', 'group', 'photo', 'created_by')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'group': {'required': True}
        }

    def validate_password(self, password):
        '''
        Method for password validation
        '''
        if len(password) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters")
        if len(password) > 32:
            raise serializers.ValidationError("password must be max 32 characters")
        if str(password).isalpha() or str(password).isnumeric():
            raise serializers.ValidationError("password must contain at least alphabets and numbers")
        return password

    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        if data['group']  is not None:
            group = UserGroup.objects.get(id=data["group"])
            group_data = GetGroupSerializer(group)
            data['group'] =  group_data.data
        return data

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers \
                .ValidationError({"password": "Password fields didn't match."})

        if attrs['group'] is None or attrs['group'] == '':
            raise serializers.ValidationError(
                {"group": "Please provide group"})

        return attrs


    def validate_user_name(self, value):
        '''
        Method for user_name validation
        '''
        small_case_value = value.lower()
        if small_case_value != value:
            raise serializers.ValidationError(
                {"user_name": "username does not support Uppercase Letters."})
        if " " in value:
            raise serializers.ValidationError(
                {"user_name": "username does not support blank character."})
        return value

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        validated_data['created_by'] = current_user.get_created_by(self.context)
        user = User.objects.create_user(**validated_data, user_type=1)
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    '''
    serializer for user login
    '''
    user_name = serializers.CharField(max_length=50, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=4, write_only=True
    )
    tokens = serializers.SerializerMethodField()
   
    def get_tokens(self, obj):
        user = User.objects.get(user_name=obj['user_name'])
        request = self.context.get('request', None)
        user_tokens = user.tokens(request)
        return {
            # 'refresh': user.tokens(request)['refresh'],
            'refresh': user_tokens['refresh'],
            # 'access': user.tokens(request)['access']
            'access': user_tokens['access']
        }

    class Meta:
        model = User
        fields = ['id', 'user_name', 'password',
                  'group', 'tokens', 'is_superuser', 'photo','email' ,'first_name','middle_name','last_name','address','birth_date','mobile_no','gender']
        depth = 2
        read_only_fields = ['password', 'group','tokens','email', 'is_superuser', 'photo']

    def validate(self, attrs):
        '''
        Method for validate user_name and password for user login
        '''
        # request = self.context.get('request')
        user_name = attrs.get('user_name', '')
        password = attrs.get('password', '')
        # group = self.get('group', '')
        user = authenticate(user_name=user_name, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        return {
            'user_name': user.user_name,
            'tokens': user.tokens,
            'id': user.id,
            'group': user.group,
            'is_superuser': user.is_superuser,
            'photo': user.photo,
            'first_name':user.first_name,
            'middle_name':user.middle_name,
            'last_name':user.last_name,
            'address':user.address,
            'birth_date':user.birth_date,
            'mobile_no' : user.mobile_no,
            'gender':user.gender


           
        }


class LogoutSerializer(serializers.Serializer):
    '''
    serializer for user logout
    '''
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except:
            raise serializers.ValidationError({"bad token"})


class ChangePasswordSerializer(serializers.ModelSerializer):
    '''
    serializer class for change password for user
    '''
    password = serializers.CharField(
        write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'confirm_password')
        extra_kwargs = {
            'old_password': {'required': True},
            'password': {'required': True},
            'confirm_password': {'required': True}
        }

    def validate_password(self, password):
        '''
        Method for validate user password
        '''
        if len(password) < 6:
            serializers.ValidationError("Password must be at least 6 characters")
        if len(password) > 32:
            serializers.ValidationError("password must be max 32 characters")
        if str(password).isalpha():
            serializers.ValidationError("password must contain at least alphabets and numbers")
        return password

    def validate(self, attrs):
        user = self.context['request'].user
        try:
            if not user.check_password(attrs['old_password']):
                raise serializers \
                    .ValidationError(
                        {"old_password": "Old password is not correct"}
                    )
        except KeyError:
            raise serializers.ValidationError(
                {'key_error': 'please provide old_password'})

        try:
            if attrs['password'] != attrs['confirm_password']:
                raise serializers \
                    .ValidationError({"password": "Password fields didn't match."})
        except KeyError:
            raise serializers.ValidationError(
                {'key_error': 'please provide password and confirm_password'})
        return attrs

    def update(self, instance, validated_data):
        '''
        function for update password for user
        '''
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    '''
    serializer class update user
    '''
    photo = serializers.ImageField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
    email = serializers.EmailField(required=True)
    user_name = serializers.CharField(required=True)
    user_group_name = serializers.ReadOnlyField(
        source='group.name', allow_null=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'middle_name', 'last_name', 'email', 'user_name', 'active',
                  'gender', 'birth_date', 'address', 'mobile_no', 'photo', 'group', 'user_group_name')
        read_only_fields = ['id']

    def validate_email(self, value):
        '''
        Method for validate Email
        '''
        pk = self.context['pk']
        if User.objects.exclude(pk=pk).filter(email=value).exists():
            raise serializers.ValidationError(
                {"email": "This email is already in use."})
        return value

    def validate_user_name(self, value):
        '''
        Method for validate username
        '''
        pk = self.context['pk']
        if User.objects.exclude(pk=pk).filter(user_name=value).exists():
            raise serializers.ValidationError(
                {"user_name": "This username is already in use."})
        small_case_value = value.lower()
        if small_case_value != value:
            raise serializers.ValidationError(
                {"user_name": "username does not support Uppercase Letters."})
        if " " in value:
            raise serializers.ValidationError(
                {"user_name": "username does not support blank character."})
        return value

    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        if data['group']  is not None:
            group = UserGroup.objects.get(id=data["group"])
            group_data = GetGroupSerializer(group)
            data['group'] =  group_data.data
        return data