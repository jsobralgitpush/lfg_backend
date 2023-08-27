from django.contrib import admin
from eav.forms import BaseDynamicEntityForm
from eav.admin import BaseEntityAdmin
from .models import Proposal


class ProposalAdminForm(BaseDynamicEntityForm):
    model = Proposal


class ProposalAdmin(BaseEntityAdmin):
    model = ProposalAdminForm


admin.register(Proposal, ProposalAdmin)
