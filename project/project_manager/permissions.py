from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Autorise la lecture à tout le monde,
    mais limite les modifications à l'auteur de l'objet.
    """
    message = "Vous devez être le proprietaire du projet pour le modifier."
    def has_object_permission(self, request, view, obj):
        """
        Vérifie les permissions sur un objet précis.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class IsOwner(permissions.BasePermission):
    """
    Limite les modifications au proprietaire de l'objet.
    """
    message = "Vous devez être le proprietaire du projet pour le modifier."
    def has_object_permission(self, request, view, obj):
        """
        Vérifie les permissions sur un objet précis.
        """
        return obj.owner == request.user


class IsAdminOrIsAuthor(permissions.BasePermission):
    """
    Autorise la lecture à tout le monde,
    mais limite les modifications aux administrateurs et au proprietaire.
    """
    message = "Vous devez être administrateur pour modifier."
    def has_object_permission(self, request, view, obj):
        """
        Vérifie les permissions sur un objet précis.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        elif obj.owner == request.user:
            return True
        elif request.user.is_staff == True:
            return True
        return False


class IsUser(permissions.BasePermission):
    """
    Autorise la lecture à tout le monde,
    mais limite les modifications au proprietaire du compte.
    """
    message = "Vous devez être le proprietaire de ce compte pour le modifier."
    def has_object_permission(self, request, view, obj):
        """
        Vérifie les permissions sur un compte utilisateur.
        """
        return obj.pk == request.user.pk


class IsAdminOrIsUser(permissions.BasePermission):
    """
    Limite la suppression d'un compte aux administrateurs ou au proprietaire du compte.
    """
    message = "Vous devez être administrateur pour modifier."
    def has_object_permission(self, request, view, obj):
        """
        Vérifie les permissions sur un objet précis.
        """
        if obj.pk == request.user.pk:
            return True
        elif request.user.is_staff == True:
            return True
        return False
    