from django.urls import path
from .views import ProposalAttributesView

app_name = 'proposal'

urlpatterns = [
    path('attributes', ProposalAttributesView.as_view(), name='attributes'),
]
