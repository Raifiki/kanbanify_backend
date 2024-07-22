
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from board.views import BoardViewSet, CategoryViewSet, TaskViewSet
from kanbanifyauth.views import LoginView, UserViewSet

router = routers.DefaultRouter() # router anlegen
router.register(r'kanbanify/v1/board', BoardViewSet) # defineiren der urls im router 
router.register(r'kanbanify/v1/category', CategoryViewSet) # defineiren der urls im router 
router.register(r'kanbanify/v1/task', TaskViewSet) # defineiren der urls im router 
router.register(r'kanbanify/v1/user', UserViewSet) # defineiren der urls im router 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('kanbanify/v1/login/', LoginView.as_view()),
    path('',include(router.urls)) # einbinden aller URLS des routers
]
