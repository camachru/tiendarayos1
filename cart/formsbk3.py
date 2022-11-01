from django import forms
from .models import OrderItem, ColourVariation, Product, SizeVariation, Address, DjangoPostalcodesMexicoPostalcode
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
        model = DjangoPostalcodesMexicoPostalcode
        fields = ['d_codigo']
        
    def clean(self):
        cpostal1 = self.cleaned_data['d_codigo']
        cpostal2 = DjangoPostalcodesMexicoPostalcode.objects.get(d_codigo=cpostal1)
        
        
        if not cpostal2:
            raise forms.ValidationError(f"Código Postal no existe ")


class AddressForm(forms.Form):

    selected_shipping_address = forms.ModelChoiceField(
        Address.objects.none(), required=True
    )
    print(selected_shipping_address) 
    

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        super().__init__(*args, **kwargs)

        user = User.objects.get(id=user_id)

        shipping_address_qs = Address.objects.filter(
            user=user,
            address_type='S'
        )
        print(shipping_address_qs)

        self.fields['selected_shipping_address'].queryset = shipping_address_qs




class AddressForm2(forms.Form):
    # tipo_dom = forms.CharField(required=false)
    calle =  forms.CharField(required=True)
    # no_ext =  forms.CharField(required=True)
    # no_int =  forms.CharField(required=false)
    # telefono =  forms.CharField(required=false)
    # Indicaciones =  forms.TextField(blank=True, null=True)
    

    
    
    # ver AddToCartForm



    selected_colonia = forms.ModelChoiceField(queryset=DjangoPostalcodesMexicoPostalcode.objects.none())
   
    print(selected_colonia)
    

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        cpostalk = kwargs.pop('cpostalk')
        

        super().__init__(*args, **kwargs)

        user = User.objects.get(id=user_id)



        # shipping_address_qs = Address.objects.filter(
        #     user=user,
        #     address_type='S'
        # )

         

        cpostalz = DjangoPostalcodesMexicoPostalcode.objects.filter(d_codigo="15400")

        print(cpostalz, cpostalk)
        
        # self.fields['selected_colonia'].queryset = cpostalz

        
        
    def clean(self):
        data = self.cleaned_data

        # selected_colonia_address = data.get('selected_colonia', None)
        

        




    
        
        

        
        
