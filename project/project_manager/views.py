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
from .permissions import IsAuthorOrReadOnly, IsAdminOrIsAuthor, IsUser, IsAdminOrIsUser, IsOwner


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
            permission_classes = [IsAdminOrIsAuthor]
        elif self.action in ['put', 'patch']:
            permission_classes = [IsOwner]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]



    '''def get_project_owner(self):
        """
        Récupère le proprietaire du projet si la route est imbriquée.
        Si la route n'est pas imbriquée, retourne None.
        """
        owner = self.kwargs.get('project_pk')
        if project_pk is None:
            return None
        return get_object_or_404(Project, pk=project_pk)

    def get_queryset(self):
        queryset = super().get_queryset()
        project = self.get_parent_project()
        if project is not None:
            queryset = queryset.filter(project=project.pk)
        return queryset

    @action(
        detail=True,
        methods=['GET', 'PATCH', 'DELETE'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def modify_project(self, request):
        """Récupère les détails d’un projet spécifique (lecture publique).
        Permet également la modification ou suppression d’un projet, uniquement par son propriétaire (en fonction du username)."""
        queryset = self.get_queryset().filter(pk=self.get_parent_project().pk)
        self.serializer_class = ProjectSerializer
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)'''



class ModifyProjectAPIView(APIView):
    """Vue pour que le proprietaire d'un projet puisse le modifier"""
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
        project = self.get_object(pk)
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

    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
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

    '''@action(detail=True, methods=['PUT', 'PATCH', 'DELETE'], permission_classes=[IsUserOrReadOnly])
    def user_details(self, request):
        user = self.get_object()
        self.serializer_class = UserSerializer
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)'''

    



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
        queryset = Project.objects.all()
        project = self.get_parent_project()
        if project is not None:
            queryset = queryset.filter(project=project.pk)
        return queryset


    @action(
        detail=True,
        methods=['GET', 'PUT', 'PATCH', 'DELETE']
    )
    def modify_project(self, request):
        """Récupère les détails d’un projet spécifique (lecture publique).
        Permet également la modification ou suppression d’un projet, uniquement par son propriétaire (en fonction du username)."""
        queryset = self.get_queryset().filter(pk=self.get_parent_project().pk)
        self.serializer_class = ProjectSerializer
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)'''
    



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
