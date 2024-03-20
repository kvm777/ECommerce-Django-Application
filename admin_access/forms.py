from django.forms import ModelForm
from store.models import *

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','digital','image']

