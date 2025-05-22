from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from app.views import *


routr = routers.DefaultRouter()
routr.register(r'accounts',accountsView,'accounts')

ro = routers.DefaultRouter()
routr.register(r'details',DetailseView,'details')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(routr.urls)),
    path('',include(ro.urls)),
    path('login/',LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('service-availability/<int:service_id>/', ServiceAvailabilityView.as_view(), name='service-availability'),
    path('bookings/', BookingCreateView.as_view(), name='create-booking'),
    path('services/<str:service_name>/bookings/', ServiceBookingsView.as_view(), name='service-bookings'),
    path('service-inquiry/', ServiceInquiryView.as_view(), name='service-inquiry'),
    

]
