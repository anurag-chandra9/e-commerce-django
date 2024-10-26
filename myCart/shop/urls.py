from django.urls import path
from.import views
urlpatterns = [
    path("",views.index,name="ShopHome"),
    path("about/",views.about,name="Aboutus"),
    path("contact/",views.contact,name="contactus"),
    path("tracker/",views.tracker,name="trackingstatus"),
    path("search/",views.search,name="search"),
    path("productview/",views.productview,name="prodView"),
    path("checkout/",views.checkout,name="checkout"),
]