from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

router = DefaultRouter()

router.register(r'projects', views.ProjectViewSet, basename='project')
router.register(r'users', views.UserViewSet, basename='user')


urlpatterns =[
    path('', include(router.urls)),
    path('projects/<int:pk>/<str:username>/', views.ModifyProjectAPIView.as_view(), name='modify_project')
]