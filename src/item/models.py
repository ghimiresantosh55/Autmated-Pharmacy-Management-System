'''
model for item app
'''
# django libraries import
from django.core.exceptions import ValidationError
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files import File
from easy_care import settings
# User-defined models (import)
from src.core_app.models import CreateInfoModel
from django.core.validators import MinValueValidator, MaxValueValidator
from src.company.models import Company
from src.supplier.models import Supplier
from typing import Optional, Collection

# import for log
from simple_history import register
from log_app.models import LogBase

def upload_path_item(instance, filename):
    return '/'.join(['item_image', filename])


def validate_image(image):
    '''
    Function for validate image size for upload
    '''
    file_size = image.size
    limit_byte_size = settings.MAX_UPLOAD_SIZE
    if file_size > limit_byte_size:
        # converting into kb
        f = limit_byte_size / 1024
        # converting into MB
        f = f / 1024
        raise ValidationError("Max size of file is %s MB" % f)


class Unit(CreateInfoModel):
    '''
    model for unit
    '''
    name = models.CharField(max_length=50, unique=True,\
                            help_text="Unit name can be max. of 50 characters and must be unique")
    short_form = models.CharField(max_length=20,unique=True,\
                            help_text="short_form can be max. of 20 characters and must be unique")
    display_order = models.IntegerField(default=0, blank= True, null= True, help_text="Display order for ordering, default=0,blank= True, null= True")
    active = models.BooleanField(default=True, help_text="By default active=True")

    def __str__(self):
        return "id {} : {}".format(self.id, self.name)

    def validate_unique(self, exclude: Optional[Collection[str]] = ...) -> None:

      # Custom unique validation check for case insensitive
        if self.id:
           if Unit.objects.exclude(id=self.id).filter(name__iexact=self.name).exists():
             raise ValidationError("this Unit name already exists")
        else:
           if Unit.objects.filter(name__iexact=self.name).exists():
              raise ValidationError("this unit  name already exists")
        return super().validate_unique(exclude)


register(Unit, app="log_app", table_name="item_Unit_log", custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])



class ItemUnit(CreateInfoModel):
    '''
    model for  product unit
    '''
    name = models.CharField(max_length=50, unique=True,\
                            help_text=" Product Unit name can be max. of 50 characters and must be unique")
    short_form = models.CharField(max_length=20,unique=True,\
                            help_text="short_form can be max. of 20 characters and must be unique")
    display_order = models.IntegerField(default=0, blank= True, null= True, help_text="Display order for ordering, default=0,blank= True, null= True")
    active = models.BooleanField(default=True, help_text="By default active=True")

    def __str__(self):
        return "id {} : {}".format(self.id, self.name)


    def validate_unique(self, exclude: Optional[Collection[str]] = ...) -> None:

      # Custom unique validation check for case insensitive
        if self.id:
           if ItemUnit.objects.exclude(id=self.id).filter(name__iexact=self.name).exists():
             raise ValidationError("this ItemUnit name already exists")
        else:
           if ItemUnit.objects.filter(name__iexact=self.name).exists():
              raise ValidationError("this itemunit name already exists")
        return super().validate_unique(exclude)


register(ItemUnit, app="log_app", table_name="item_product_Unit_log", custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])



class MedicineCategory(CreateInfoModel):
    '''
    model for medicine category
    '''
    name = models.CharField(max_length=100, unique=True,
                            help_text="Medicine category name should be max. of 100 characters")

    active = models.BooleanField(default=True, help_text="By default= True")
    archived = models.BooleanField(default=False, help_text="By default= False")
   
    def __str__(self):
        return "id {}".format(self.id)


    def validate_unique(self, exclude: Optional[Collection[str]] = ...) -> None:

      # Custom unique validation check for case insensitive
        if self.id:
           if MedicineCategory.objects.exclude(id=self.id).filter(name__iexact=self.name).exists():
             raise ValidationError("this Medicine Category name already exists")
        else:
           if MedicineCategory.objects.filter(name__iexact=self.name).exists():
              raise ValidationError("this Medicine Category name already exists")
        return super().validate_unique(exclude)
        
register(MedicineCategory, app="log_app", table_name="medicine_category_log", custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])



class Strength(CreateInfoModel):
    '''
    model for strength
    '''
    strength = models.CharField(max_length=50,blank = True, null=True, help_text="strength name should be max. of 50 characters and blank = True, null= True")
    unit= models.ForeignKey(Unit, on_delete=models.PROTECT, blank = True, null = True, help_text= "null = true , blank = true")
    active = models.BooleanField(default=True, help_text="By default active=True")
    archived = models.BooleanField(default=False, help_text="By default= False")

    class Meta:
      unique_together = ('strength', 'unit',)

    def __str__(self):
        return "id {}".format(self.id)

register(Strength, app="log_app", table_name="strength_log", custom_model_name=lambda x: f'Log{x}',
    use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
    excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])




class GenericName(CreateInfoModel):
    '''
    model for generic name
    '''
    PRESCRIPTION_NEEDED = (
        (1, "YES"),
        (2, "NO")
       
    )
    name = models.CharField(max_length=150, unique=True,
                            help_text="Generic name should be max. of 150 characters")
    medicine_category = models.ManyToManyField(MedicineCategory, related_name ="medicine_categories")
    prescription_needed = models.BooleanField(default=True, help_text="By default active=True")
    uses = models.TextField()
    side_effects = models.TextField()
    concerns  = models.TextField()
    indications= models.TextField()
    active = models.BooleanField(default=True, help_text="By default active=True")
    archived = models.BooleanField(default=False, help_text="By default= False")

    def __str__(self):
        return "id {} : {}".format(self.id, self.name)


    def validate_unique(self, exclude: Optional[Collection[str]] = ...) -> None:

      # Custom unique validation check for case insensitive
        if self.id:
           if GenericName.objects.exclude(id=self.id).filter(name__iexact=self.name).exists():
             raise ValidationError("this Generic name already exists")
        else:
           if GenericName.objects.filter(name__iexact=self.name).exists():
              raise ValidationError("this Generic name already exists")
        return super().validate_unique(exclude)


register(GenericName, app="log_app", table_name="item_genericname_log", custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])



class SuperCategory(CreateInfoModel):
    '''
    model for super category
    '''
    name = models.CharField(max_length=100, unique=True,
                            help_text="super category name should be max. of 100 characters")
    image = image = models.ImageField(upload_to="super_category", validators=[validate_image], blank=True)
    #webp
    image_webp = models.ImageField(upload_to="super_category/webp", validators=[validate_image], blank=True, null=True)
    #png
    image_png = models.ImageField(upload_to="super_category/png", validators=[validate_image], blank=True, null= True)
    active = models.BooleanField(default=True, help_text="By default= True")
    archived = models.BooleanField(default=False, help_text="By default= False")

    def __str__(self):
        return "id {}".format(self.id)


    def validate_unique(self, exclude: Optional[Collection[str]] = ...) -> None:

      # Custom unique validation check for case insensitive
        if self.id:
           if SuperCategory.objects.exclude(id=self.id).filter(name__iexact=self.name).exists():
             raise ValidationError("this Super Category name already exists")
        else:
           if SuperCategory.objects.filter(name__iexact=self.name).exists():
              raise ValidationError("this Super Category name already exists")
        return super().validate_unique(exclude)


    def save(self,*args,**kwargs):
        '''
        this method will convert image into web and png format
        '''
        if  self.image:
            img = Image.open(self.image).convert('RGB')
            im_io = BytesIO()
            img.save(im_io, format="webp")

            # new_image= File(im_io_sm,name="%s.webp"%self.image.name.split('.')[0],)
            image_webp= File(im_io, name="%s.webp"%self.image.name.split('.')[-1],)
            self.image_webp = image_webp
        
            image_png= File(im_io, name="%s.png"%self.image.name.split('.')[-1],)
            self.image_png = image_png
        else:
            self.image_webp=""
            self.image_png=""

        super().save(*args,**kwargs)

register(SuperCategory, app="log_app", table_name="super_category_log", custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])




class ProductCategory(CreateInfoModel):
    '''
    model for product category
    '''
    name = models.CharField(max_length=100, unique=True,
                            help_text="product category name should be max. of 100 characters")
    super_category = models.ForeignKey(SuperCategory, on_delete=models.PROTECT)
    is_medicine = models.BooleanField(default=False, help_text="By default= False")
    image = models.ImageField(upload_to="product_category", validators=[validate_image], blank=True)
    #webp
    image_webp = models.ImageField(upload_to="product_category/webp", validators=[validate_image], blank=True, null=True)
    #png
    image_png = models.ImageField(upload_to="product_category/png", validators=[validate_image], blank=True, null= True)
    active = models.BooleanField(default=True, help_text="By default= True")
    archived = models.BooleanField(default=False, help_text="By default= False")

    def __str__(self):
        return "id {}".format(self.id)


    def validate_unique(self, exclude: Optional[Collection[str]] = ...) -> None:

      # Custom unique validation check for case insensitive
        if self.id:
           if ProductCategory.objects.exclude(id=self.id).filter(name__iexact=self.name).exists():
             raise ValidationError("this Product Category name already exists")
        else:
           if ProductCategory.objects.filter(name__iexact=self.name).exists():
              raise ValidationError("this Product Category name already exists")
        return super().validate_unique(exclude)


    def save(self,*args,**kwargs):
        '''
        this method will convert image into web and png format
        '''
        if  self.image:
            img = Image.open(self.image).convert('RGB')
            im_io = BytesIO()
            img.save(im_io, format="webp")
            # new_image= File(im_io_sm,name="%s.webp"%self.image.name.split('.')[0],)
            image_webp= File(im_io, name="%s.webp"%self.image.name.split('.')[-1],)
            self.image_webp = image_webp 
            image_png= File(im_io, name="%s.png"%self.image.name.split('.')[-1],)
            self.image_png = image_png
        else:
            self.image_webp=""
            self.image_png=""
        super().save(*args,**kwargs)

register(ProductCategory, app="log_app", table_name="product_category_log", custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])



class MedicineForm(CreateInfoModel):
    '''
    model for medicineform
    '''
    name = models.CharField(max_length=50, unique=True,
                            help_text="name should be max. of 50 characters")
    active = models.BooleanField(default=True, help_text="By default active=True")
    archived = models.BooleanField(default=False, help_text="By default= False")

    def __str__(self):
        return "id {}".format(self.id)


    def validate_unique(self, exclude: Optional[Collection[str]] = ...) -> None:

      # Custom unique validation check for case insensitive
        if self.id:
           if MedicineForm.objects.exclude(id=self.id).filter(name__iexact=self.name).exists():
             raise ValidationError("this Medicine Form  name already exists")
        else:
           if MedicineForm.objects.filter(name__iexact=self.name).exists():
              raise ValidationError("this Medicine form name already exists")
        return super().validate_unique(exclude)


register(MedicineForm, app="log_app", table_name="medicine_form_log", custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])



class GenericStrength(models.Model):
  '''
  GenericStrength Model
  '''
  strength = models.ForeignKey(Strength, on_delete=models.PROTECT)
  generic_name =  models.ForeignKey(GenericName, on_delete=models.PROTECT, related_name="generic_strength")
  archived = models.BooleanField(default=False, help_text="By default= False")

  def __str__(self):
        return "id {}".format(self.id)
                            


class Item(CreateInfoModel):
    '''
    model for item
    '''
    product_category = models.ManyToManyField(ProductCategory,blank = True)
    brand_name = models.CharField(max_length=200, unique=True,
                            help_text="brand name should be max. of 100 characters")
    item_unit = models.ForeignKey(ItemUnit, null = True, on_delete=models.PROTECT,\
                             help_text= "item unit foreign key references from ItemUnit model")

    ws_unit = models.IntegerField(blank = True, null = True)
    generic_name = models.ManyToManyField(GenericStrength, blank = True)
    item_details = models.TextField(null=True, blank=True)
    medicine_form = models.ForeignKey(MedicineForm, on_delete=models.PROTECT, blank=True, null = True)
    company =  models.ForeignKey(Company, null = True, on_delete=models.PROTECT, related_name = 'items')
    code = models.CharField(max_length=10, unique=True,  blank=True,
                            help_text="Item code should be max. of 10 characters")
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.0,
                                    help_text="Max value  price can be upto 9999999999.99, price means MRP")

    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0,
                                   help_text= "default=0.0 and can be upto 100.00")
    image = models.ImageField(upload_to = "item/image", validators=[validate_image], blank=True)
    verified = models.BooleanField(default=True, help_text="By default active=True")
    purchase_qty = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text="Null= True, blank =True")
    free_qty = models.IntegerField(null=True, blank=True,  validators=[MinValueValidator(0), MaxValueValidator(100)], help_text="Null= True, blank =True")
    active = models.BooleanField(default=True, help_text="By default active=True")
    archived = models.BooleanField(default=False, help_text="By default= False")

    def __str__(self):
        return "id {}".format(self.id)


    def save(self, *args, **kwargs):
      if self.image=="":
        self.image=""
  
      return super().save(*args, **kwargs)


    # def update(self,*args,**kwargs):
    #   print("hello")   
    #   if "image" not in self:
    #         self.image=""  
    #   super().save(*args,**kwargs)
    

    def validate_unique(self, exclude: Optional[Collection[str]] = ...) -> None:

      # Custom unique validation check for case insensitive
        if self.id:
           if Item.objects.exclude(id=self.id).filter(brand_name__iexact=self.brand_name).exists():
             raise ValidationError("this  Item  brand name already exists")
        else:
           if Item.objects.filter(brand_name__iexact=self.brand_name).exists():
              raise ValidationError("this Item brand name already exists")
        return super().validate_unique(exclude)


register(Item, app="log_app", table_name="item_log", custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])



class PoPriority(CreateInfoModel):
    '''
    model class for Purchase Order Priority
    '''
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='po_priorities')
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    priority = models.IntegerField(validators = [MaxValueValidator(15), MinValueValidator(1),]) 
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0,
                                   help_text= "default=0.0 and can be upto 100.00")                          
    active = models.BooleanField(default=True, help_text="By default active=True")
    archived = models.BooleanField(default=False, help_text="By default= False")

    # class Meta:
    #     unique_together = ('supplier', 'company'), ('priority','company')
        
    def __str__(self):
        return "id {}".format(self.id)

register(PoPriority, app="log_app", table_name="po_priority_log", custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])
