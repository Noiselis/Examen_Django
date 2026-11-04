from rest_framework import serializers
#from django.contrib.auth.hashers import check_password, make_password, is_password_usable
#from django.contrib.auth.password_validation import validate_password,  password_changed, password_validators_help_texts, password_validators_help_text_html
#from django.contrib.auth.forms import UserCreationForm
from .models import User, Project
#import re


'''class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)'''


class UserSerializer(serializers.ModelSerializer):
    """
    Serialiseur pour l'affichage et la modification du compte utilisateur de l'utilisateur connecte
    Serialiseur pour les utilisateurs
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        read_only_fields = ['id']     # Non modifiable avec PUT ou PATCH

    #validate_password(password=User.password)
    #make_password(password=User.password)

    '''def validate_username(self, value):
        """
        Vérifie que le nom de l'utilisateur comporte au moins 2 caractères utiles
        et qu'il ne contient pas uniquement des chiffres.
        """
        cleaned_value = value.strip()
        if len(cleaned_value) < 2:
            raise serializers.ValidationError(
                "Le nom d'utilisateur doit contenir au moins 2 caractères."
            )
        if cleaned_value.isdigit():
            raise serializers.ValidationError(
                "Le nom d'utilisateur ne peut pas contenir uniquement des chiffres."
            )
        return value

    def validate_email(self, value):
        """Verifie que l'email n'est pas juste compose d'espaces"""
        if value:
            if not value.strip():
                raise serializers.ValidationError("L'email ne peut pas être vide.")
            return value
        raise serializers.ValidationError("L'email ne peut pas être vide.")'''
            


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serialiseur pour les projets
    """
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'created_at', 'owner']
        read_only_fields = ['id', 'created_at', 'owner']     # Non modifiable avec PUT ou PATCH




'''class RegisterSerializer(serializers.ModelSerializer):
    """
    Serialiseur pour la creation d'un compte utilisateur
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        read_only_fields = ['id']     # Non modifiable avec PUT ou PATCH

    validate_password(password=User.password)
    make_password(password=User.password)

    def validate_username(self, value):
        """
        Vérifie que le nom de l'utilisateur comporte au moins 2 caractères utiles
        et qu'il ne contient pas uniquement des chiffres.
        """
        cleaned_value = value.strip()
        if len(cleaned_value) < 2:
            raise serializers.ValidationError(
                "Le nom d'utilisateur doit contenir au moins 2 caractères."
            )
        if cleaned_value.isdigit():
            raise serializers.ValidationError(
                "Le nom d'utilisateur ne peut pas contenir uniquement des chiffres."
            )
        return value

    def validate_email(self, value):
        """Verifie que l'email n'est pas juste compose d'espaces"""
        if not value.strip():
            raise serializers.ValidationError("L'email ne peut pas être vide.")
        return value'''