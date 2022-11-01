from django import forms
from django.forms import MultipleChoiceField
from .models import OrderItem, ColourVariation, Product, SizeVariation, Address, addresses
from django.contrib.auth import get_user_model
 

User = get_user_model()


class AddToCartForm(forms.ModelForm):
    colour = forms.ModelChoiceField(queryset=ColourVariation.objects.none())
    size = forms.ModelChoiceField(queryset=SizeVariation.objects.none())
    quantity = forms.IntegerField(min_value=1)

    class Meta:
        model = OrderItem
        fields = ['quantity', 'colour', 'size']
        

    def __init__(self, *args, **kwargs):
        self.product_id = kwargs.pop('product_id')
        product = Product.objects.get(id=self.product_id)
        super().__init__(*args, **kwargs)

        self.fields['colour'].queryset = product.available_colours.all()
        self.fields['size'].queryset = product.available_sizes.all()

    def clean(self):
        product_id = self.product_id
        product = Product.objects.get(id=self.product_id)
        quantity = self.cleaned_data['quantity']

        if product.stock < quantity:
            raise forms.ValidationError(f"The maximum stock is {product.stock}")

class ValCpostalForm(forms.ModelForm):
    d_codigo = forms.CharField( label="Códico Postal",max_length=5 )
    

    class Meta:
        model = addresses
        fields = ['d_codigo']
        
    def clean(self):
        cpostal1 = self.cleaned_data['d_codigo']
        cpostal2 = addresses.objects.filter(d_codigo=cpostal1)
        
        if not cpostal2:
            raise forms.ValidationError(f"Código Postal no existe ")







class AddressForm2(forms.Form):    
    selected_colonia = forms.ModelChoiceField(addresses.objects.none(), required=False )
    tipo_dom = forms.CharField(required=False)
    calle =  forms.CharField(required=False)
    no_ext =  forms.CharField(required=False)
    no_int =  forms.CharField(required=False)
    telefono =  forms.CharField(required=False)
    Indicacionesa =  forms.CharField(widget=forms.Textarea, required=False)
    
    

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        self.cpostalk = kwargs.pop('cpostalk1')  
        
        super().__init__(*args, **kwargs)
        user = User.objects.get(id=user_id)
        cpostalz = addresses.objects.filter(d_codigo=self.cpostalk)
        
        self.fields['selected_colonia'].queryset = cpostalz
        

        

class AddressForm(forms.Form):

    selected_shipping_address = forms.ModelChoiceField(
        Address.objects.none(), required=True
    )
    
    

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        super().__init__(*args, **kwargs)

        user = User.objects.get(id=user_id)

        shipping_address_qs = Address.objects.filter(
            user=user
             )
        
        

        self.fields['selected_shipping_address'].queryset = shipping_address_qs        




    
        
        

        
        
