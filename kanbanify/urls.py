
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from board.views import BoardViewSet, CategoryViewSet, TaskViewSet

router = routers.DefaultRouter() # router anlegen
router.register(r'board', BoardViewSet) # defineiren der urls im router 
router.register(r'category', CategoryViewSet) # defineiren der urls im router 
router.register(r'task', TaskViewSet) # defineiren der urls im router 

urlpatterns = [
    path('admin/', admin.site.urls),
     path('',include(router.urls)) # einbinden aller URLS des routers
]
