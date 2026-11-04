from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User, Project
#from .serializers import CustomUserCreationForm


#admin.site.register(User, CustomUserAdmin)
#admin.site.register(User, UserAdmin)
admin.site.register(User)
admin.site.register(Project)
#admin.site.register(CustomUserCreationForm)




