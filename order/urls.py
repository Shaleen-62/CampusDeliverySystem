from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('update-cart/<int:f_id>', views.update_cart, name='update-cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('myorders/', views.my_orders, name='my-orders'),
    path('search/', views.search_results, name='search_results'),
    path('logout/', views.user_logout, name='logout'),
    path('delivery_agent/', views.delivery_agent, name='delivery_agent'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)