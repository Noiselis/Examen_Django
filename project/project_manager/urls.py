from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

router = DefaultRouter()

router.register(r'projects', views.ProjectViewSet, basename='project')
router.register(r'users', views.UserViewSet, basename='user')

project_router = routers.NestedDefaultRouter(
    router,
    r'projects',
    lookup='project'
)
project_router.register(
    r'user',
    views.UserViewSet,
    basename='project_owner'
)

'''project_router = routers.NestedDefaultRouter(
    router,
    r'projects',
    lookup='project'
)
project_router.register(
    r'user',
    views.ProjectUpdateViewSet,
    basename='project_owner'
)'''


urlpatterns =[
    path('', include(router.urls)),
    path('', include(project_router.urls)),
]