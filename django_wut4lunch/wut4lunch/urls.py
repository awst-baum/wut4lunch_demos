from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'lunches', views.LunchViewSet)

urlpatterns = [
    path('', views.index, name='home'),
    path('newlunch/', views.newlunch, name='newlunch'),

    path('rest/', include(router.urls)),
    path('rest-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^login/$', auth_views.login, {'template_name': 'auth/login.html'}, name='login'),    
    url(r'^logout/$', auth_views.logout, {'next_page': '/login/'}, name='logout'),    
    url(r'^admin/', admin.site.urls),
]
