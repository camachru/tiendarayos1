from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'cart'



urlpatterns = [
    path('', views.CartView.as_view(), name='summary'),
    path('shop/', views.ProductListView.as_view(), name='product-list'),
    path('shop/<slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('increase-quantity/<pk>/', views.IncreaseQuantityView.as_view(), name='increase-quantity'),
    path('decrease-quantity/<pk>/', views.DecreaseQuantityView.as_view(), name='decrease-quantity'),
    path('remove-from-cart/<pk>/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('checkout1/', login_required(views.CheckoutView1.as_view()), name='checkout1'),   
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('thank-you/', views.ThankYouView.as_view(), name='thank-you'),
    path('confirm-order/', views.ConfirmOrderView.as_view(), name='confirm-order'),
    path('orders/<pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    
    path('postal/', views.PostalView.as_view(), name='Postal-View'), 
    path('pcod/<cpostal>/', login_required(views.CheckoutView2.as_view()), name='checkout3')  
]       