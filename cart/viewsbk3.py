import datetime
import json
from django.views import generic
from django.db.models import Q
from .utils import get_or_set_order_session
from .models import Product, OrderItem, Address, Payment, Order, DjangoPostalcodesMexicoPostalcode
from .forms import  AddToCartForm, AddressForm, ValCpostalForm, AddressForm2
from django.shortcuts import get_object_or_404, reverse, redirect
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin




class ProductListView(generic.ListView):
    template_name='cart/product_list.html'    
    model=Product
    
    def get_queryset(self):
        qs = Product.objects.all()
        seleccion = self.request.GET.get('buscar')
        if seleccion:
            qs = qs.filter(Q(title__icontains=seleccion) |
                           Q(descritption__icontains=seleccion) |
                           Q(primary_category__name__icontains=seleccion) |
                           Q(secondary_categories__name__icontains=seleccion)
                           
                           )
        return qs

    # def get_context_data(self, **kwargs):
    #     context = super(ProductListView, self).get_context_data(**kwargs)
    #     context.update({
    #         "categories": Category.objects.all()
    #     })
    #     return context


class ProductDetailView(generic.FormView):
    template_name = 'cart/product_detail.html'
    form_class = AddToCartForm
    
    def get_object(self):
        return get_object_or_404(Product, slug=self.kwargs["slug"])

    def get_success_url(self):
        return reverse("cart:summary")

    def get_form_kwargs(self):
        kwargs = super(ProductDetailView, self).get_form_kwargs()
        kwargs["product_id"] = self.get_object().id
        return kwargs

    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        product = self.get_object()
        
        item_filter = order.items.filter(
            product=product,
            colour=form.cleaned_data['colour'],
            size=form.cleaned_data['size']
        )
        itemr = item_filter.first()
        

        if item_filter.exists():
            item = item_filter.first()
            item.quantity += int(form.cleaned_data['quantity'])
            item.save()
            
            

        else:
            
            new_item = form.save(commit=False)                       
            new_item.product = product
            new_item.order = order           
            new_item.save()
            
             
            
        
        return super(ProductDetailView, self).form_valid(form)


    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['product'] = self.get_object()
        return context


class CartView(generic.TemplateView):
    template_name = 'cart/cart.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context["order"] = get_or_set_order_session(self.request)
        return context


class IncreaseQuantityView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        order_item.quantity += 1
        order_item.save()
        return redirect("cart:summary")


class DecreaseQuantityView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])

        if order_item.quantity <= 1:
            order_item.delete()
        else:
            order_item.quantity -= 1
            order_item.save()
        return redirect("cart:summary")


class RemoveFromCartView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        order_item.delete()
        return redirect("cart:summary")



class CheckoutView1(generic.FormView):
    template_name = 'cart/checkout1.html'
    form_class = AddressForm

    def get_success_url(self):
        return reverse("cart:payment")

    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        selected_shipping_address = form.cleaned_data.get('selected_shipping_address')
        

        if selected_shipping_address:
            order.shipping_address = selected_shipping_address
        
        order.save()



        messages.info(
            self.request, "You have successfully added your addresses")
        return super(CheckoutView1, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CheckoutView1, self).get_form_kwargs()
        kwargs["user_id"] = self.request.user.id
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CheckoutView1, self).get_context_data(**kwargs)
        context['order'] = get_or_set_order_session(self.request)
        return context
  


class PaymentView(generic.TemplateView):
    template_name = 'cart/payment.html'

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        context["PAYPAL_CLIENT_ID"] = settings.PAYPAL_CLIENT_ID
        context['order'] = get_or_set_order_session(self.request)
        context['CALLBACK_URL']= self.request.build_absolute_uri(reverse("cart:thank-you"))
        return context


class ConfirmOrderView(generic.View):
    def post(self, request, *args, **kwargs):
        order = get_or_set_order_session(request)
        body = json.loads(request.body)
        payment = Payment.objects.create(
            order=order,
            successful=True,
            raw_response = json.dumps(body),
            amount = float(body["purchase_units"][0]["amount"]["value"]),
            payment_method='PayPal'
        )
        order.ordered = True
        order.ordered_date = datetime.date.today()
        order.save()
        return JsonResponse({"data": "Success"})


class ThankYouView(generic.TemplateView):
    template_engine = 'cart/thanks.html'


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'order.html'
    queryset = Order.objects.all()
    context_object_name = 'order'



class PostalView(generic.View):
    template_name = 'cart/cpostal.html'
    form_class = ValCpostalForm

    def get_context_data(self, **kwargs):
        contexto = {}
        contexto ['form']= self.form_class
        return contexto

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cpostal=form.cleaned_data['d_codigo'],
            request.session['cpostal'] = cpostal
            return redirect('cart:checkout3')            
        
            
    
    
    
class CheckoutView2(generic.FormView):
    template_name = 'cart/checkout2.html'
    form_class = AddressForm2

    def get_success_url(self):
        return reverse("cart:payment")

    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        selected_colonia_address = form.cleaned_data.get('selected_colonia_address')
        

        
        order.shipping_address = selected_colonia_address
        

        
        order.save()
        messages.info(
            self.request, "You have successfully added your addresses")
        return super(CheckoutView2, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CheckoutView2, self).get_form_kwargs()
        kwargs["user_id"] = self.request.user.id
        cpostal = self.request.session['cpostal']
        kwargs["cpostalk"] = cpostal
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CheckoutView2, self).get_context_data(**kwargs)
        context['order'] = get_or_set_order_session(self.request)
        return context
            

        
        
        
    
            



    