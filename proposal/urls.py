from django.urls import re_path
from .views import ProposalList, ProposalRetrieveView, ProposalAttributesView

app_name = 'proposal'

urlpatterns = [
    re_path(r'^$', ProposalList.as_view(), name='list-create'),
    re_path(r'^(?P<pk>\d+)/$', ProposalRetrieveView.as_view(), name='retrieve'),
    re_path(r'^attributes/$', ProposalAttributesView.as_view(), name='attributes'),
]
