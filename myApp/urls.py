"""myApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import imp
from django.contrib import admin
from django.urls import path,include
from web import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.root, name='root'),
    path('admin/', admin.site.urls),
    path('web/', views.index, name='index'),
    path('web/signup', views.signup, name='signup'),
    path('web/signin', views.signin, name='signin'),
    path('web/signout', views.signout, name='signout'),
    path('web/home', views.home, name='home'),
    path('web/products', views.products, name='products'),
    path('web/item', views.item, name='item'),
    path('web/main', views.main, name='main'),
    path('web/cart', views.cart, name='cart'),
    path('web/contact', views.contact, name='contact'),
    path('web/summary', views.summary, name='summary'),
    path('web/product_view', views.product_view, name='product_view'),
    path('web/allproducts', views.allproducts, name='allproducts'),
    path('web/packages', views.packages, name='packages'),
    path('web/vegetable', views.vegetable, name='vegetable'),
    path('web/fruit', views.fruit, name='fruit'),
    path('web/oil', views.oil, name='oil'),
    path('web/snack', views.snack, name='snack'),
    path('web/spice', views.spice, name='spice'),
    path('web/legumes', views.legumes, name='legumes'),
    path('updatecart', views.updateCart, name='updatecart'),



 
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
