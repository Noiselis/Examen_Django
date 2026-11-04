from django.shortcuts import render
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.views.generic.edit import UpdateView, CreateView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action

from .models import Project, User
from .serializers import ProjectSerializer, UserSerializer
from .pagination import CustomPagination


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

    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    '''def perform_create(self, serializer):
        """Assigne automatiquement l'utilisateur connecté comme proprietaire"""
        serializer.save(owner=self.request.user)'''



class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les utilisateurs
    """
    queryset = User.objects.all().order_by("-id")

    serializer_class = UserSerializer

    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    '''def get_parent_project(self):
        """
        Récupère le projet parent si la route est imbriquée.
        Si la route n'est pas imbriquée, retourne None.
        """
        project_pk = self.kwargs.get('project_pk')
        if project_pk is None:
            return None
        return get_object_or_404(Project, pk=project_pk)

    def get_queryset(self):
        queryset = super().get_queryset()
        project = self.get_parent_project()
        if project is not None:
            queryset = queryset.filter(project=project.pk)
        return queryset'''

    '''@action(
        detail=True,
        methods=['GET', 'PATCH', 'DELETE'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def view_modify_project(self, request):
        """Récupère les détails d’un projet spécifique (lecture publique).
        Permet également la modification ou suppression d’un projet, uniquement par son propriétaire (en fonction du username)."""
        queryset = self.get_queryset().filter(pk=self.get_parent_project().pk)
        self.serializer_class = ProjectSerializer
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)'''
    

    '''def get_permissions(self):
        """
        Instancie et renvoie la liste des permissions requises
        selon l'action du ViewSet.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]'''



'''class RegisterViewSet(CreateView):
    """
    ViewSet pour creer un compte
    """
    model = User
    fields = ["username", "email", "password"]


class ProjectUpdateViewSet(UpdateView):
    """
    ViewSet pour modifier ou supprimer un projet par son proprietaire
    """
    model = Project
    fields = ["title", "description"]
    template_name_suffix = "_update_form"'''
