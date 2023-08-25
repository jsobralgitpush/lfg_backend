from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomAttribute


@admin.register(CustomAttribute)
class CustomAttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)
