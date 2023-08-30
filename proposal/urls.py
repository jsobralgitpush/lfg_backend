from django.urls import path
from .views import ProposalAttributesView, ProposalList, ProposalRetrieveView

app_name = 'proposal'

urlpatterns = [
    path('', ProposalList.as_view(), name='list-create'),
    path('<int:pk>/', ProposalRetrieveView.as_view(), name='retrieve'),
    path('attributes', ProposalAttributesView.as_view(), name='attributes'),
]
