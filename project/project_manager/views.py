from django.shortcuts import render
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.hashers import check_password, make_password, is_password_usable

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action

from .models import Project, User
from .serializers import ProjectSerializer, UserSerializer
from .pagination import CustomPagination
from .permissions import IsOwnerOrReadOnly, IsAdminOrIsOwnerOrReadOnly, IsUser, IsAdminOrIsUser, IsOwner


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les projets
    """
    queryset = Project.objects.all().order_by("-created_at", "-id")

    serializer_class = ProjectSerializer

    pagination_class = CustomPagination

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]
    filterset_fields = ['owner']
    search_fields = ['title', 'description']
    ordering_fields = ['id', 'title', 'created_at', 'owner']

    def perform_create(self, serializer):
        """Assigne automatiquement l'utilisateur connecté comme proprietaire du projet"""
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """
        Instancie et renvoie la liste des permissions requises
        selon l'action du ViewSet.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'destroy':
            permission_classes = [IsAdminOrIsOwnerOrReadOnly]
        elif self.action in ['put', 'patch']:
            permission_classes = [IsOwner]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class ModifyProjectAPIView(APIView):
    """Vue d'un projet pour que le proprietaire puisse le modifier"""
    def get_object(self, pk):
        project = Project.objects.get(pk=pk)
        try :
            return project
        except project.DoesNotExist():
            raise Http404("Projet introuvable")

    def get(self, request, pk, username):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk, username):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid() and username == request.user.username:
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, username):
            project = self.get_object(pk)
            serializer = ProjectSerializer(project, data=request.data, partial=True)
            if serializer.is_valid() and username == request.user.username:
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, username):
        project = self.get_object(pk)
        if username == request.user.username or request.user.is_staff == True:
            project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise PermissionError('Vous devez etre un admin ou le proprietaire pour supprimer ce projet')



class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les utilisateurs
    """
    queryset = User.objects.all().order_by("-id")

    serializer_class = UserSerializer

    lookup_field = 'username'
    
    def get_permissions(self):
        """
        Instancie et renvoie la liste des permissions requises
        selon l'action du ViewSet.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.IsAdminUser]
        elif self.action == 'destroy':
            permission_classes = [IsAdminOrIsUser]
        elif self.action in ['put', 'patch']:
            permission_classes = [IsUser]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['POST'], url_path='register', permission_classes = [permissions.AllowAny])
    def register_user(self, request):
        self.serializer_class = UserSerializer
        print(request.data)
        print(request.data['password'])
        request.data['password'] = make_password(request.data['password'])
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

