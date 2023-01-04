from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from  src.blood_test.models import BloodTest, BloodTestCategory
from src.company.models import Company
from src.customer.models import Customer
from src.item.models import Item, GenericStrength, MedicineCategory, ProductCategory, SuperCategory
from src.item.serializers import GetProductSerializer
from django.utils import timezone
from django.db.models import Sum
from src.sale.models import SaleDetail
from src.customer_order.serializers import GetItemSerializer

User = get_user_model()

class GetItemForSupeSaleSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Item
        fields=['image']


class GetSuperCategorySerializer(serializers.ModelSerializer):
    '''
    Get serializer class for super category
    '''
    class Meta:
        model = SuperCategory
        exclude=['archived','active','image' ,'image_webp','image_png','created_date_ad', 'created_date_bs',
        'created_by', 'app_type','device_type']  



class GetProductCategorySerializer(serializers.ModelSerializer):
      class Meta:
        model = ProductCategory
        exclude=['archived','active','image' ,'image_webp','image_png','created_date_ad', 'created_date_bs',
        'created_by', 'app_type','device_type']  


class GetMedicineCategorySerializer(serializers.ModelSerializer):
      class Meta:
        model = MedicineCategory
        exclude=['archived','active','created_date_ad', 'created_date_bs',
        'created_by', 'app_type','device_type']  


class  GetCompanyFeatureBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields=['id','name','brand_image']



class GetGenericNameSerializer(serializers.ModelSerializer):
    '''
    model serializer for get  generic name data
    '''
    strength_unit =  serializers.ReadOnlyField(source="strength.unit.name", allow_null=True)
    strength_value = serializers.ReadOnlyField(source="strength.strength", allow_null=True)
    generic_name_name = serializers.ReadOnlyField(source="generic_name.name", allow_null=True)
    generic_name_uses= serializers.ReadOnlyField(source="generic_name.uses", allow_null=True)
    generic_name_side_effects=serializers.ReadOnlyField(source="generic_name.side_effects", allow_null=True)
    generic_name_concerns=serializers.ReadOnlyField(source="generic_name.concerns", allow_null=True)

    class Meta:
        model = GenericStrength
        exclude=['archived','strength','generic_name']  


class RegisterPublicUserSerializer(serializers.ModelSerializer):
    
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
                  'address', 'mobile_no',  'photo')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
           
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

   
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers \
                .ValidationError({"password": "Password fields didn't match."})

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
        # validated_data['created_by'] = current_user.get_created_by(self.context)
        user = User.objects.create_user(**validated_data, user_type=2)                         
        user.save()
        return user



class PublicUserLoginSerializer(serializers.ModelSerializer):
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
                   'tokens', 'is_superuser', 'photo','email' ,'first_name','middle_name','last_name','address','birth_date','mobile_no','gender']
        depth = 2
        read_only_fields = ['password', 'tokens','email', 'is_superuser', 'photo']

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



class PublicUserListSerializer(serializers.ModelSerializer):
    user_group_name = serializers.ReadOnlyField(
        source='group.name', allow_null=True)
    # user=  RegisterUserCustomerSerializer()
   
    class Meta:
        model = User
        exclude = ['password','groups','user_type']

    def to_representation(self, instance):
        '''
        Method for add extra key value pair
        '''
        my_fields = {'birth_date', 'created_by', 'user_group_name'}
        data = super().to_representation(instance)
        for field in my_fields:
            try:
                if not data[field]:
                    data[field] = ""
            except KeyError:
                pass
        return data


class PublicUserChangePasswordSerializer(serializers.ModelSerializer):
    '''
    serializer class for change password for public user
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
        instance.set_password(validated_data['password'])
        instance.save()
        return instance



class PublicUserLogoutSerializer(serializers.Serializer):
    '''
    serializer for public user logout
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


class GetSuperCategorySerializer(serializers.ModelSerializer):
     class Meta:
                model = SuperCategory
                exclude = ['created_date_ad','created_date_bs','created_by','active', 'archived',\
                    'device_type','app_type' ]


class GetProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
                model = ProductCategory
                exclude = ['created_date_ad','created_date_bs','created_by','active', 'archived',\
                    'device_type','app_type','super_category']


class GetMedicineItemSerializer(serializers.ModelSerializer):
        item_unit_name = serializers.ReadOnlyField(source='item_unit.name', allow_null = True)
        item_unit_short_form_name = serializers.ReadOnlyField(source='item_unit.short_form', allow_null= True)
        medicine_form_name=  serializers.ReadOnlyField(source='medicine_form.name', allow_null= True)
        company_name = serializers.ReadOnlyField(source='company.name', allow_null= True)
      
        class Meta:
                model = Item
                exclude = ['created_date_ad','created_date_bs','created_by','active', 'free_qty','purchase_qty','archived',\
                    'verified','device_type','app_type' ]


        def to_representation(self, instance):
            data =  super().to_representation(instance)
            data["generic_name"] = GetGenericNameSerializer(instance.generic_name.all(), many=True).data

            return data


class HomePageAppItemSerializer(serializers.ModelSerializer):
    
    class Meta:
            model = Item
            exclude = ['created_date_ad','created_date_bs','created_by','active', 'free_qty','purchase_qty','archived','generic_name',\
                    'verified','device_type','app_type', 'medicine_form', 'company','item_unit']

    def to_representation(self, instance):
        '''
        To representation method of Item
        '''
        data =  super().to_representation(instance)
        data["product_category"] = GetProductSerializer(instance.product_category.all(), many=True).data
        return data


class FeatureBrandItemSerializer(serializers.ModelSerializer): 
    company_name = serializers.ReadOnlyField(source= 'company.name', allow_null = True)
    class Meta:
            model = Item
            exclude = ['created_date_ad','created_date_bs','created_by','active', 'free_qty','purchase_qty','archived','generic_name',\
                    'verified','device_type','app_type', 'medicine_form', 'item_unit' ]

    def to_representation(self, instance):
        '''
        To representation method of Item
        '''
        data =  super().to_representation(instance)
        data["product_category"] = GetProductSerializer(instance.product_category.all(), many=True).data

        if data['company']  is not None:
            company = Company.objects.get(id=data["company"])
            company_data =  GetCompanyFeatureBrandSerializer(company, allow_null = True)
            data['company'] =   company_data.data
        return data



class  GetbloodTestCategorySerializer(serializers.ModelSerializer): 
    class Meta:
        model = BloodTestCategory
        exclude = ['created_date_ad','created_date_bs','created_by','active','device_type','app_type']
                   


class GetBloodTestSerializer(serializers.ModelSerializer):
    
    class Meta:
            model = BloodTest
            exclude = ['created_date_ad','created_date_bs','active','created_by','device_type','app_type']
                    

    def to_representation(self, instance):
        '''
        '''
        data =  super().to_representation(instance)
        data["blood_test_category"] = GetbloodTestCategorySerializer(instance.blood_test_category.all(), many=True).data
        return data


class ListPublicUserSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = User
        fields = ('id','user_name','mobile_no', 'email' ,'first_name', 'last_name','address')


class ListCustomerSerializer(serializers.ModelSerializer):
    
    user =  ListPublicUserSerializer()
    class Meta:
        model = Customer
        exclude = ['created_date_ad', 'created_date_bs']
 
   


class BetterDiscountItemSerializer(serializers.ModelSerializer):
        item_unit_name = serializers.ReadOnlyField(source='item_unit.name', allow_null = True)
        item_unit_short_form_name = serializers.ReadOnlyField(source='item_unit.short_form', allow_null= True)
        medicine_form_name=  serializers.ReadOnlyField(source='medicine_form.name', allow_null= True)
        company_name = serializers.ReadOnlyField(source='company.name', allow_null= True)
  
      
        class Meta:
                model = Item
                exclude = ['created_date_ad','created_date_bs','created_by','active', 'free_qty','purchase_qty','archived',\
                    'verified','device_type','app_type' ]


        def to_representation(self, instance):
            data =  super().to_representation(instance)
            data["generic_name"] = GetGenericNameSerializer(instance.generic_name.all(), many=True).data

            return data


class MostSaleItemSerializer(serializers.ModelSerializer):
        #item_id= serializers.ReadOnlyField(source='item.id', allow_null = True)
        item_unit_name = serializers.ReadOnlyField(source='item.item_unit.name', allow_null = True)
        item_unit_short_form_name = serializers.ReadOnlyField(source='item.item_unit.short_form', allow_null= True)
        company_name = serializers.ReadOnlyField(source='item.company.name', allow_null= True)
        brand_name= serializers.ReadOnlyField(source='item.brand_name', allow_null= True)
        item_details = serializers.ReadOnlyField(source='item.item_details', allow_null= True)
        total_sale_qty=serializers.SerializerMethodField()
        class Meta:
                model = SaleDetail
                exclude = ['created_date_ad','created_date_bs','created_by','device_type','app_type','qty','sale_main','id']


        def get_total_sale_qty(self, instance):
            sale_item=instance.item
            total_sale_qty = sum(
            SaleDetail.objects.filter(created_date_ad__year=timezone.now().year, item=sale_item,sale_main__sale_type=1).values_list('qty',flat=True))
            return  total_sale_qty


        def to_representation(self, instance):
            data =  super().to_representation(instance)
            item = Item.objects.get(id=data["item"])
            image_data = GetItemForSupeSaleSerializer(item, allow_null = True)
            data['image'] =  image_data.data
            return data
            