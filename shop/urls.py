
from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name="ShopHome"),
    path('about', views.about, name="About"),
    path('contact', views.contact, name="Contact"),
    path('tracker', views.tracker, name="Tracker"),
    path('search/', views.search, name="Search"),
    path('product/<int:myid>', views.product, name="ProuctView"),
    path('checkout', views.checkOut, name="CheckOut"),
    path('cart', views.cart, name="Cart"),
    path('Feedback', views.feedback, name="Feedback"),
    path('handlerequest', views.handlerequest, name="handlerequest"),
    # path('paymentstatus', views.paymentstatus, name="paymentstatus"),
]
