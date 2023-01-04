
from pickle import TRUE
from rest_framework import  serializers

from src.customer_order.serializers import  GetUserForCustomerSerializer
from src.user_group.models import UserGroup
# imported model here
from .models import Customer

from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.db import transaction
from django.utils import timezone
from src.user.models import User

# User = get_user_model()

class CustomerListSerializer(serializers.ModelSerializer):
    '''
    Model serializer for get customer list
    ''' 
    user_name = serializers.ReadOnlyField(source='user.user_name',allow_null =TRUE)
    class Meta:
        model = Customer
        fields = "__all__"
    
    def to_representation(self, instance):
        '''
        representation method for user object
        '''
        data =  super().to_representation(instance)
        
        if data['user']  is not None:
            user = User.objects.get(id=data["user"])
            user_data = GetUserForCustomerSerializer(user)
            data['user'] = user_data.data
        return data


class RegisterPublicUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required= False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    user_name = serializers.CharField(
        min_length=4, max_length=50, required=True, allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(max_length=50, required = False
    )
    last_name = serializers.CharField(max_length=50, required=False
    )
    address = serializers.CharField(max_length=100, required= False
    )

    password = serializers.CharField(
        write_only=True, required= True, min_length=6
    )
    confirm_password = serializers.CharField(write_only=True, required= True)
    
 
    class Meta:
        model = User
        fields = ('user_name', 'first_name', 'last_name', 'address', 'password', 'email','confirm_password','active')
       

    def validate_password(self, password):
        '''
        method for validate password
        '''
        if len(password) < 6:
            serializers.ValidationError("Password must be at least 6 characters")
        if len(password) > 32:
            serializers.ValidationError("password must be max 32 characters")
        if str(password).isalpha():
            serializers.ValidationError("password must contain at least alphabets and numbers")
        return password


    def validate(self, attrs):
            if attrs['password'] != attrs['confirm_password']:
                raise serializers \
                    .ValidationError({"password": "Password fields didn't match."})
            return attrs


    def validate_user_name(self, value):
        '''
        method for validate user name
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
        user = User.objects.create_user(**validated_data, user_type = 2, group= UserGroup.objects.get(id= 6))
        user.save()
        return user


class RegisterPublicCustomerSerializer(serializers.ModelSerializer):
    '''
    model serializer for register customer
    '''
    user = RegisterPublicUserSerializer()
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['created_date_ad', 'created_date_bs']


    @transaction.atomic
    def create(self, validated_data):
        '''
        This method will create or register customer
        '''
        # print(validated_data,"this is validated data")
        user_serializer = RegisterPublicUserSerializer(data=validated_data.pop('user'))
        if user_serializer.is_valid(raise_exception=True):
           user = user_serializer.save()
        if validated_data['client_no'] == "" or validated_data['client_no'] is None:
            """
            This will auto generate client number
            """
            clientnum_count = Customer.objects.count()
            client_id = str(clientnum_count + 1)
            unique_id = "CID-" + client_id.zfill(3)
            validated_data['client_no'] = unique_id
        customer= Customer.objects.create(**validated_data,  user=user)
        customer.save()
        return customer



class RegisterUserCustomerSerializer(serializers.ModelSerializer):
    '''
    model serializer for register user customer 
    '''
    email = serializers.EmailField(
        required= False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    user_name = serializers.CharField(
        min_length=4, max_length=50, required=True, allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
 
    password = serializers.CharField(
        write_only=True, required= True, min_length=6
    )
    confirm_password = serializers.CharField(write_only=True, required= True)
    
 
    class Meta:
        model = User
        fields = ('user_name', 'password', 'email','confirm_password','active')
       

    def validate_password(self, password):
        '''
        method for validate password
        '''
        if len(password) < 6:
            serializers.ValidationError("Password must be at least 6 characters")
        if len(password) > 32:
            serializers.ValidationError("password must be max 32 characters")
        if str(password).isalpha():
            serializers.ValidationError("password must contain at least alphabets and numbers")
        return password


    def validate(self, attrs):
            if attrs['password'] != attrs['confirm_password']:
                raise serializers \
                    .ValidationError({"password": "Password fields didn't match."})
            return attrs


    def validate_user_name(self, value):
        '''
        method for validate user name
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
        user = User.objects.create_user(**validated_data, user_type = 2, group= UserGroup.objects.get(id= 6))
        user.save()
        return user
        

class RegisterCustomerSerializer(serializers.ModelSerializer):
    '''
    model serializer for register customer
    '''
    user = RegisterUserCustomerSerializer()
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['created_date_ad', 'created_date_bs']


    @transaction.atomic
    def create(self, validated_data):
        '''
        This method will create or register customer
        '''
        user_serializer = RegisterUserCustomerSerializer(data=validated_data.pop('user'))
        if user_serializer.is_valid(raise_exception=True):
           user = user_serializer.save()
        if validated_data['client_no'] == "" or validated_data['client_no'] is None:
            """
            This will auto generate client number
            """
            clientnum_count = Customer.objects.count()
            client_id = str(clientnum_count + 1)
            unique_id = "CID-" + client_id.zfill(3)
            validated_data['client_no'] = unique_id
        customer= Customer.objects.create(**validated_data,  user=user)
        customer.save()
        return customer

   
class UpdateCustomerUserSerializer(serializers.ModelSerializer):
    '''
    model serializer for update user customer
    '''
    email = serializers.EmailField(required=False)
    user_name = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ('user_name', 'password','email' ,'confirm_password')

    def validate_password(self, password):
        '''
        Method for validate user password
        '''
        if password is not None:
            if len(password) < 6:
                serializers.ValidationError("Password must be at least 6 characters")
            if len(password) > 32:
                serializers.ValidationError("password must be max 32 characters")
            if str(password).isalpha():
                serializers.ValidationError("password must contain at least alphabets and numbers")
        return password


    def validate_email(self, value):
        '''
        Method for validate user email
        '''
        pk = self.context['pk']
        if User.objects.exclude(pk=pk).filter(email=value).exists():
            raise serializers.ValidationError(
                    {"email": "This email is already in use."})
        return value
        

    def validate(self, attrs):
        if 'password' in attrs:
            if attrs['password'] !=attrs['confirm_password']:
                 raise serializers \
                        .ValidationError({"password": "Password fields didn't match."})
        return attrs
        

    def validate_user_name(self, value):
        '''
        Method for validate user name
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

        
       
    def update(self, instance, validated_data):
        '''
        method for update password for user
        '''
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.user_name = validated_data.get('user_name', instance.user_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance
    

class UpdateCustomerSerializer(serializers.ModelSerializer):
    '''
    serializer class for update customer
    '''
    user = UpdateCustomerUserSerializer()
    class Meta:
        model = Customer
        exclude = ['created_date_ad', 'created_date_bs']
 
    @transaction.atomic
    def update(self, instance, validated_data):
        '''
        this method will update customer
        '''
        user_instance = instance.user
        user_serializer =  UpdateCustomerUserSerializer(user_instance, data=validated_data.pop('user'),  partial = True, context={
                                                                                                 'pk': user_instance.id})
        if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()
      
        customer_serializer = CustomerListSerializer(instance,  data=validated_data, partial=True)
        if  customer_serializer.is_valid(raise_exception=True):
            customer_serializer.save()
        return super().update(instance, validated_data)

    
         


    
