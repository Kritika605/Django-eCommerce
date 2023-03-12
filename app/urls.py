from django.urls import path,include
from . import views
from .forms import LoginForm,MyPasswordChangeForm , MyPasswordResetForm, MySetPasswordForm
from django.contrib.auth import views as auth_view

urlpatterns = [   
    path('', views.ProductView.as_view(), name = "home"),    
    path('product_detail/<int:pk>', views.ProductDetailView.as_view(), name = "product_detail"),  

    path('search/', views.SearchView.as_view(), name = "search"),    

    path('login/', auth_view.LoginView.as_view(authentication_form = LoginForm,
    template_name = "app/login.html"), name = "login"),    

    path('logout/', auth_view.LogoutView.as_view(next_page = "login"), name = "logout"), 
    path('register/', views.CustomerRegistrationView.as_view(), name = "customerregistration"), 

    # Password Url
    path('changepassword/', auth_view.PasswordChangeView.as_view(form_class = MyPasswordChangeForm ,template_name ="app/changepassword.html"
    ,success_url = "/changepassworddone/"), name = "changepassword"),    

    path('changepassworddone/', auth_view.PasswordChangeDoneView.as_view(template_name = "app/changepassworddone.html"), name = "changepassworddone"),  

    path('password_reset/', auth_view.PasswordResetView.as_view(template_name = "app/password_reset.html",form_class = MyPasswordResetForm), name = "password_reset"),    
    path('password_reset/done/', auth_view.PasswordResetDoneView.as_view(template_name = "app/password_reset_done.html"), name = "password_reset_done"),    

    path("reset/<uidb64>/<token>/",auth_view.PasswordResetConfirmView.as_view(template_name = "app/password_reset_confirm.html",
    form_class = MySetPasswordForm),name="password_reset_confirm"),

    path("password_reset/complete/",auth_view.PasswordResetCompleteView.as_view(template_name = "app/password_reset_complete.html"),name="password_reset_complete"),


   
    path('profile/', views.CustomerProfileView.as_view(), name = "profile"),    
    path('orders/', views.OrdersView.as_view(), name = "orders"),    
    path('address/', views.AddressView.as_view(), name='address'),
    path('mobile/', views.MobileView.as_view(), name='mobile'),
    path('laptop/', views.LaptopView.as_view(), name='laptop'),
    path('men_topwear/', views.MenTopWearView.as_view(), name='men_topwear'),
    path('men_bottomwear/', views.MenBottomWearView.as_view(), name='men_bottomwear'),
    path('women_topwear/', views.WomenTopWearView.as_view(), name='women_topwear'),
    path('women_bottomwear/', views.WomenBottomWearView.as_view(), name='women_bottomwear'),

    # Cart Url  
    path('add-to-cart/', views.Add_to_cart.as_view(), name='add-to-cart'),
    path('show-cart/', views.ShowCart.as_view(), name='show-cart'),
    path('pluscart/', views.pluscart, name='pluscart'),
    path('minuscart/', views.minuscart, name='minuscart'),
    path('remove_cart/', views.remove_cart, name='remove_cart'),
    path('placeorder/', views.placeorder, name='placeorder'),
    path('payment_done/', views.payment_done, name='payment_done'),
    


]
