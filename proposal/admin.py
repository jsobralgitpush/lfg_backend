from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Proposal, CustomAttribute, CustomAttributeValue


class CustomAttributeValueInline(admin.TabularInline):
    model = CustomAttributeValue
    extra = 1


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    inlines = [CustomAttributeValueInline]


@admin.register(CustomAttribute)
class CustomAttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)
