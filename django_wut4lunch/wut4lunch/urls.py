from django.urls import path
from django.conf.urls import include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'lunches', views.LunchViewSet)

urlpatterns = [
    path('', views.index, name='home'),
    path('newlunch/', views.newlunch, name='newlunch'),

    path('rest/', include(router.urls)),
    path('rest-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
