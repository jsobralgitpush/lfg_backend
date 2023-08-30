from rest_framework import mixins
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .serializers import AttributeSerializer, ProposalSerializer
from .models import Proposal
from .tasks import send_proposal_task
from eav.models import Attribute

# Create your views here.


class ProposalAttributesView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProposalList(generics.ListCreateAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        document = request.data.get('document')
        eav_data = {k: v for k, v in request.data.items() if k not in [
            'name', 'document']}

        proposal = Proposal(name=name, document=document)

        for key, value in eav_data.items():
            setattr(proposal.eav, f'{key.lower()}', f'{value}')

        proposal.status = 'pending_by_system'

        proposal.save()
        send_proposal_task.delay(name, document, proposal.id)

        serializer = self.get_serializer(proposal)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProposalRetrieveView(generics.RetrieveAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
