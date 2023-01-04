from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class Location(MPTTModel):
    """
    Inventory Location table implemented with MPTT
    """
    name = models.CharField(
        max_length=100, verbose_name=_("location name"), help_text=_("format: required, max-100")
    )
    is_active = models.BooleanField(default=True)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, related_name="children", null=True, blank=True, verbose_name=_("parent of location"))
    
    class Meta:
        verbose_name = _("Product Location")
        verbose_name_plural = _("product Location")
    
    def __str__(self):
        return f"{self.id} : {self.name}"
