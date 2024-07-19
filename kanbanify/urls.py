
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from board.views import BoardViewSet

router = routers.DefaultRouter() # router anlegen
router.register(r'board', BoardViewSet) # defineiren der urls im router 

urlpatterns = [
    path('admin/', admin.site.urls),
     path('',include(router.urls)) # einbinden aller URLS des routers
]
