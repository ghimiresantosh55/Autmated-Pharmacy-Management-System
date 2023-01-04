'''
serializer for item app
'''
# django imports here
from rest_framework import serializers
#imported model here
from .models import  GenericStrength, MedicineForm, Unit,  GenericName, Item, ItemUnit, \
PoPriority, Strength
from .models import ProductCategory, SuperCategory, MedicineCategory
from src.supplier.models import Supplier
from src.company.models import Company
from src.custom_lib.functions import current_user
from django.utils import timezone
from django.db.models import Max


ITEM_CODE_LENGTH = 5


class GetItemSerializer(serializers.ModelSerializer):
    '''
    Get serializer for item
    '''
    item_unit_name = serializers.ReadOnlyField(source='item_unit.name', default = "")
    company_name =  serializers.ReadOnlyField(source='company.name', allow_null=True)
    company_discount_rate = serializers.ReadOnlyField(source='company.discount_rate', allow_null=True)
 
    class Meta:
        model = Item
        exclude = ['created_date_ad','created_date_bs','active','image','created_by','product_category' ,'generic_name',\
                            'device_type','app_type','medicine_form','free_qty','item_details','archived']



class GetItemUnitSerializer(serializers.ModelSerializer):
    '''
    get serializer class for Get ItemUnit
    '''
    class Meta:
        model = ItemUnit
        exclude = ['created_date_ad','created_date_bs','active','display_order','created_by', 'device_type','app_type']


class GetUnitSerializer(serializers.ModelSerializer):
    '''
    get serializer class for GetUnit
    '''
    class Meta:
        model = Unit
        exclude = ['created_date_ad','created_date_bs','active','created_by','display_order',  'device_type','app_type']      


        
class GetMedicineCategorySerializer(serializers.ModelSerializer):

    '''
    model serializer for get product category data
    '''
    class Meta:
        model = MedicineCategory
        exclude= ['created_by', 'created_date_ad','active', 'created_date_bs','device_type','app_type','archived']


class GetStrengthSerializer(serializers.ModelSerializer):
    '''
    model serializer for get product category data
    '''
    unit_name = serializers.ReadOnlyField(source="unit.name", allow_null=True)
    class Meta:
        model = Strength
        exclude= ['created_by', 'created_date_ad','active', 'created_date_bs','device_type','app_type', 'unit']


class GetProductSerializer(serializers.ModelSerializer):
    '''
    model serializer for get product category data
    '''
    # super_category_name = serializers.ReadOnlyField(source="super_category.name", allow_null=True)
    class Meta:
        model = ProductCategory
        exclude= ['image', 'active','created_by', 'created_date_ad', 'created_date_bs','device_type','app_type','archived','image_webp','image_png']


    def to_representation(self, instance):
        '''
        method for get objects
        '''
        data =  super().to_representation(instance)
       
        if data['super_category']  is not None:
            super_category = SuperCategory.objects.get(id=data["super_category"])
            super_category_data = GetSuperCategorySerializer( super_category)
            data['super_category'] =  super_category_data.data
        return data


class ReadOnlyGenericNameSerializer(serializers.ModelSerializer):
    '''
    model serializer for get  generic name data
    '''
    strength_unit =  serializers.ReadOnlyField(source="strength.unit.name", allow_null=True)
    strength_value = serializers.ReadOnlyField(source="strength.strength", allow_null=True)
    generic_name_name = serializers.ReadOnlyField(source="generic_name.name", allow_null=True)

    class Meta:
        model = GenericStrength
        fields = "__all__"



class GetSuperCategorySerializer(serializers.ModelSerializer):
    '''
    Model serializer for get super category data
    '''
    class Meta:
        model = SuperCategory
        exclude = ['created_by', 'created_date_ad', 
        'created_date_bs','device_type','app_type', 'active','archived']



class UnitSerializer(serializers.ModelSerializer):
    '''
    model serializer for unit
    '''
    class Meta:
        model = Unit
        fields = "__all__"
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs']

    def create(self, validated_data):
        date_now = timezone.now()
        validated_data['created_by'] = current_user.get_created_by(self.context)
        unit = Unit.objects.create(**validated_data, created_date_ad=date_now)
        return unit


class ItemUnitSerializer(serializers.ModelSerializer):
    '''
    model serializer for  product unit
    '''
    class Meta:
        model = ItemUnit
        fields = "__all__"
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs','device_type','app_type',]

    def create(self, validated_data):
        date_now = timezone.now()
        validated_data['created_by'] = current_user.get_created_by(self.context)
        item_unit = ItemUnit.objects.create(**validated_data, created_date_ad=date_now)
        return item_unit



class MedicineCategorySerializer(serializers.ModelSerializer):
    '''
    model serializer for medicine category
    '''
   
    device_type_display = serializers.ReadOnlyField(source="get_device_type_display", allow_null=True)
    app_type_display = serializers.ReadOnlyField(source="get_app_type_display", allow_null=True)
    # archived = serializers.BooleanField(write_only=True)
    class Meta:
        model = MedicineCategory
        exclude= ['archived']
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs','device_type','app_type', 'device_type_display','app_type_display']


    def create(self, validated_data):
        '''
        create method for medicine category
        ''' 
        date_now = timezone.now()
        validated_data['created_by'] = current_user.get_created_by(self.context)
        medicine_category = MedicineCategory.objects.create(**validated_data, created_date_ad=date_now)
        return medicine_category



class DeletePoPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model =PoPriority
        fields =  ['id','archived']     


class GenericStrengthSerializer(serializers.ModelSerializer):
    '''
    Model serializer for GenericStrength
    '''
    strength_unit = serializers.ReadOnlyField(source="strength.unit.name", allow_null=True, default = "")
    strength_value = serializers.ReadOnlyField(source="strength.strength", allow_null=True, default = "")
    generic_name_name = serializers.ReadOnlyField(source="generic_name.name", allow_null=True, default = "")
    # archived = serializers.BooleanField(write_only=True)
    
    class Meta:
        model = GenericStrength
        exclude= ['archived']


    def create(self, validated_data):
        '''
        create method for GenericStrength
        '''
        generic_strength = GenericStrength.objects.create(**validated_data)
        return generic_strength




class GenericStrengthMapSerializer(serializers.ModelSerializer):
    '''
    Model serializer for GenericStrengthMap
    '''
    unit_name =   serializers.ReadOnlyField(source="strength.unit.name", allow_null=True)
    unit_short_name =  serializers.ReadOnlyField(source="strength.unit.short_form", allow_null=True)

    class Meta:
        model = GenericStrength
        exclude = ["generic_name"]
        # depth = 1


    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['strength']  is not None: 
            strength = Strength.objects.get(id=data["strength"])
            strength_data =  StrengthSerializer(strength)
            data['strength'] = strength_data.data
        return data
        
 
class GenericNameSerializer(serializers.ModelSerializer):
    '''
    model serializer for generic name
    '''
    generic_strength = GenericStrengthMapSerializer(many=True)
    # archived = serializers.BooleanField(write_only=True)
    class Meta:
        model = GenericName
        exclude= ['archived']
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs']


    def create(self, validated_data):
        '''
        create method for generic name
        '''
        date_now = timezone.now()
        medicine_catagories = validated_data.pop('medicine_category')
        strengths =  validated_data.pop('generic_strength')
        validated_data['created_by'] = current_user.get_created_by(self.context)
        generic_name = GenericName.objects.create(**validated_data, created_date_ad=date_now)
        for medicine_category in medicine_catagories:
            generic_name.medicine_category.add(medicine_category)
        for strength in strengths:
            GenericStrength.objects.create(strength=strength['strength'], generic_name=generic_name)
        return generic_name


    def to_representation(self, instance):
        '''
        this method will get medicine category objects
        '''
        data = super().to_representation(instance)
        data["medicine_category"] = GetMedicineCategorySerializer(instance.medicine_category.all(), many=True).data
        return data



class ItemSerializer(serializers.ModelSerializer):
    '''
    Model serializer fir item
    '''

    image = serializers.ImageField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
   
    class Meta:
        model = Item
        exclude=['app_type','device_type', 'created_date_ad', 'created_date_bs','archived']
        read_only_fields = [ 'created_by', ]
       

    def create(self, validated_data):
        '''
        Create method of Item
        '''
        if validated_data['code']== "" or validated_data['code'] is None:
                item_count = Item.objects.aggregate(Max('id'))
                max_id = str(item_count['id__max'] + 1)
                unique_id = "ITM-" + max_id.zfill(ITEM_CODE_LENGTH)
                validated_data['code'] = unique_id
        else:
            validated_data['code'] = str(validated_data['code']).upper()
        date_now = timezone.now()
        product_catagories = validated_data.pop('product_category')
        generic_names =  validated_data.pop('generic_name')
        validated_data['created_by'] = current_user.get_created_by(self.context)
        item= Item.objects.create(**validated_data, created_date_ad=date_now)
        for product_category in product_catagories:
            item.product_category.add(product_category)
        if generic_names is not None:
            for generic_name in  generic_names:
                item.generic_name.add(generic_name)
        return item


    def to_representation(self, instance):
        '''
        To representation method of Item
        '''
        data = super().to_representation(instance)
        data["product_category"] = GetProductSerializer(instance.product_category.all(), many=True).data
        data["generic_name"] =  ReadOnlyGenericNameSerializer(instance.generic_name.all(), many=True).data

        if data['item_unit']  is not None: 
            item_unit = ItemUnit.objects.get(id=data["item_unit"])
            item_unit_data = GetItemUnitSerializer(item_unit)
            data['item_unit'] =  item_unit_data .data

        if data['medicine_form']  is not None:
            medicine_form = MedicineForm.objects.get(id=data["medicine_form"])
            medicine_form_data = GetMedicineFormSerializer(medicine_form)
            data['medicine_form'] = medicine_form_data.data
        
        if data['company'] is not None:
            company = Company.objects.get(id=data["company"])
            company_data = GetCompanySerializer(company)
            data['company'] =  company_data.data
        return data



class SuperCategorySerializer(serializers.ModelSerializer):
    '''
    model serializer for super category
    '''
    device_type_display = serializers.ReadOnlyField(source="get_device_type_display", allow_null=True)
    app_type_display = serializers.ReadOnlyField(source="get_app_type_display", allow_null=True)
    image = serializers.ImageField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
    # archived = serializers.BooleanField(write_only=True)
    class Meta:
        model = SuperCategory
        exclude= ['archived']
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs',
        'device_type','app_type', 'device_type_display','app_type_display','image_webp','image_png']

        

    def create(self, validated_data):
        '''
        Create Method of Super Category
        '''
        date_now = timezone.now()
        validated_data['created_by'] = current_user.get_created_by(self.context)
        super_category = SuperCategory.objects.create(**validated_data, created_date_ad=date_now)
        return super_category



class ProductCategorySerializer(serializers.ModelSerializer):
    '''
    model serializer for product category
    '''
    device_type_display = serializers.ReadOnlyField(source="get_device_type_display", allow_null=True)
    app_type_display = serializers.ReadOnlyField(source="get_app_type_display", allow_null=True)
    image = serializers.ImageField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
    # archived = serializers.BooleanField(write_only=True)

    class Meta:
        model = ProductCategory
        exclude= ['archived']
        read_only_fields = ['created_by', 'created_date_ad', 'image_png',
        'created_date_bs','device_type','app_type', 'device_type_display','app_type_display','image_webp']


    def to_representation(self, instance):
        '''
        To representation method OF Product Category
        '''
        data =  super().to_representation(instance)
        super_category = SuperCategory.objects.get(id=data["super_category"])
        super_category_data = GetSuperCategorySerializer(super_category)
        data['super_category'] = super_category_data.data
        return data


    def create(self, validated_data):
        '''
        Create Method of Product Category
        '''
        date_now = timezone.now()
        validated_data['created_by'] = current_user.get_created_by(self.context)
        product_category = ProductCategory.objects.create(**validated_data, created_date_ad=date_now)
        return product_category



class MedicineFormSerializer(serializers.ModelSerializer):
    '''
    model serializer for medicine form
    '''
    device_type_display = serializers.ReadOnlyField(source="get_device_type_display", allow_null=True)
    app_type_display = serializers.ReadOnlyField(source="get_app_type_display", allow_null=True)
    # archived = serializers.BooleanField(write_only=True)
    '''
    model serializer for super category
    '''
    class Meta:
        model = MedicineForm
        exclude= ['archived']
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs',
        'device_type','app_type', 'device_type_display','app_type_display','image_webp','image_png','archived']

    def create(self, validated_data):
        '''
        create method for medicine form
        '''
        date_now = timezone.now()
        validated_data['created_by'] = current_user.get_created_by(self.context)
        medicine_form = MedicineForm.objects.create(**validated_data, created_date_ad=date_now)
        return medicine_form



class PoPrioritySerializer(serializers.ModelSerializer):
    '''
    model serializer for medicine form
    '''
    device_type_display = serializers.ReadOnlyField(source="get_device_type_display", allow_null=True)
    app_type_display = serializers.ReadOnlyField(source="get_app_type_display", allow_null=True)
    company_name =  serializers.ReadOnlyField(source="company.name", allow_null=True)
    supplier_name = serializers.ReadOnlyField(source="supplier.name", allow_null=True)
    '''
    model serializer for super category
    '''
    class Meta:
        model = PoPriority
        exclude= ['archived']
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs',
        'device_type','app_type', 'device_type_display','app_type_display']



    def create(self, validated_data):
        date_now = timezone.now()
        validated_data['created_by'] = current_user.get_created_by(self.context)
        po_priority = PoPriority.objects.create(**validated_data, created_date_ad=date_now)
        return po_priority

     
    # def update(self, instance, validated_data):
    #     # instance.company = validated_data.get('company', instance.company)
    #     instance.supplier = validated_data.get('supplier', instance.supplier)
    #     instance.priority = validated_data.get('priority', instance.priority)
    #     if PoPriority.objects.filter(supplier=validated_data['supplier'], priority= validated_data['priority']).exists():
    #             raise serializers.ValidationError('supplier and priority should be unique together')
    #     return instance


   
class StrengthSerializer(serializers.ModelSerializer):
    '''
    model serializer for Strength
    '''
    device_type_display = serializers.ReadOnlyField(source="get_device_type_display", allow_null=True)
    app_type_display = serializers.ReadOnlyField(source="get_app_type_display", allow_null=True)
    unit_name = serializers.ReadOnlyField(source="unit.name", allow_null=True)
    unit_short_name = serializers.ReadOnlyField(source="unit.short_form", allow_null=True)
    # archived = serializers.BooleanField(write_only=True)
   
    class Meta:
        model = Strength
        exclude=['archived']
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs',
        'device_type','app_type', 'device_type_display','app_type_display']

    def create(self, validated_data):
        date_now = timezone.now()
        validated_data['created_by'] = current_user.get_created_by(self.context)
        strength = Strength.objects.create(**validated_data, created_date_ad=date_now)
        return strength



  
"""************************** Serializers for Get Views *****************************************"""


class GetGenericNameSerializer(serializers.ModelSerializer):
    '''
    get serializer class for GetGenericName
    '''
    class Meta:
        model = GenericName
        exclude = ['created_date_ad','created_date_bs','active','created_by']





class GetSupplierSerializer(serializers.ModelSerializer):
    '''
    get serializer class for Get Supplier
    '''
    class Meta:
        model = Supplier
        exclude = ['created_date_ad','created_date_bs','active','created_by', \
            'device_type','app_type']


class GetCompanySerializer(serializers.ModelSerializer):
    '''
    get serializer for get Company data
    '''
    class Meta:
        model = Company
        exclude = ['created_date_ad','created_date_bs','active','created_by',\
             'device_type','app_type','brand_image','feature_brand','phone_no','address']


class GetMedicineFormSerializer(serializers.ModelSerializer): 
    '''
    get serializer class for Get Medicine Form
    '''
    class Meta:
        model = MedicineForm
        exclude = ['created_date_ad','created_date_bs','active','created_by', \
            'device_type','app_type',]