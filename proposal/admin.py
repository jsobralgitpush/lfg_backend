from django.contrib import admin
from eav.forms import BaseDynamicEntityForm
from eav.admin import BaseEntityAdmin
from eav.models import EnumGroup, EnumValue, Value
from .models import Proposal


class ProposalEavAdminForm(BaseDynamicEntityForm):
    model = Proposal


class ProposalEavAdmin(BaseEntityAdmin):
    model = ProposalEavAdminForm


class ProposalForm(admin.ModelAdmin):
    list_display = ('id', 'name', 'document', 'status', 'last_updated')
    list_filter = ('status',)
    list_editable = ('status',)


admin.register(Proposal, ProposalEavAdmin)
admin.site.register(Proposal, ProposalForm)
admin.site.unregister(EnumValue)
admin.site.unregister(EnumGroup)
