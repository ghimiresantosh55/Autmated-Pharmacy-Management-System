from .models import BloodTest, BloodTestCategory, TestPackage
from rest_framework import  serializers
from src.custom_lib.functions import current_user
from django.utils import timezone


class  GetBloodTestCategorySerializer(serializers.ModelSerializer):

      class Meta:
        model= BloodTestCategory
        exclude = ['created_by', 'created_date_ad', 'created_date_bs','device_type','app_type','active']


class  GetBloodTestSerializer(serializers.ModelSerializer):
        class Meta:
            model= BloodTest
            exclude = ['created_by', 'created_date_ad', 'created_date_bs','device_type','app_type', 'active','blood_test_category']

        # def to_representation(self, instance):
        
        #     data = super().to_representation(instance)
        #     data["blood_test_category"] = GetBloodTestCategorySerializer(instance.blood_test_category.all(), many=True).data
        #     return data


class BloodTestCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= BloodTestCategory
        fields ="__all__"
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs','device_type','app_type']


    def create(self, validated_data):
        '''
        Create Method of blood test category
        '''
        date_now = timezone.now()
        validated_data['created_by'] = current_user.get_created_by(self.context)
        blood_test_category =  BloodTestCategory.objects.create(**validated_data, created_date_ad=date_now)
        return blood_test_category


class BloodTestSerializer(serializers.ModelSerializer):
    class Meta:
        model= BloodTest
        fields = "__all__"
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs','device_type','app_type']


    def create(self, validated_data):
        '''
        Create Method of blood test
        '''
        date_now = timezone.now()
        blood_test_categories =  validated_data.pop('blood_test_category')
        validated_data['created_by'] = current_user.get_created_by(self.context)
        blood_test =  BloodTest.objects.create(**validated_data, created_date_ad=date_now)
        if  blood_test_categories is not None:
            for blood_test_category in  blood_test_categories:
                blood_test.blood_test_category.add( blood_test_category)
     
        return blood_test

    def to_representation(self, instance):
        '''
        To representation method of Blood Test
        '''
        data = super().to_representation(instance)
        data["blood_test_category"] = GetBloodTestCategorySerializer(instance.blood_test_category.all(), many=True).data
        
        return data


class TestPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model= TestPackage
        fields = "__all__"
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs','device_type','app_type']


    def create(self, validated_data):
        '''
        Create Method of test package
        '''
        date_now = timezone.now()
        test_involves =  validated_data.pop('test_involved')
        validated_data['created_by'] = current_user.get_created_by(self.context)
        test_package =  TestPackage.objects.create(**validated_data, created_date_ad=date_now)
        if test_involves  is not None:
            for test_involved in test_involves:
                test_package.test_involved.add(test_involved)
        return test_package

    def to_representation(self, instance):
        '''
        To representation method of Test Package
        '''
        data = super().to_representation(instance)
        data["test_involved"] = GetBloodTestSerializer(instance.test_involved.all(), many=True).data

        return data



