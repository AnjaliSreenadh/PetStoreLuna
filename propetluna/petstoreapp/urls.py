
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.front, name="front"),

    path('register/',views.register,name="register"),
    path('login/',views.loginuser,name="login"),
    path('logout',views.logout,name='logout'),
    path('blog',views.blog,name='blog'),

    path('about',views.about),
    path('contact',views.contact,name='contact'),
    path('index',views.indexpage,name='index'),
    path("home",views.home,name='home'),
    path("catfilter/<cv>",views.catfilter,name='pets'),
    path("sort/<sv>",views.sort),
    # path('range',views.range),
    path("pdetails/<pid>",views.product_details),
    path('addtocart/<pid>',views.addtocart,name='addtocart'),
    path('viewcart/',views.viewcart,name='viewcart'),
    path("remove/<cid>",views.remove),
    path("updateqty/<qv>/<cid>",views.updateqty),
    path('placeorder',views.placeorder),
    path("makepayment",views.makepayment),

    path('contact-details/', views.contact, name='contact'),
    path('categories',views.filtercat,name='pets'),
    # path('process_payment/', views.process_payment, name='process_payment'),
]