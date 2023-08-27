from django.shortcuts import render
from rest_framework import mixins
from rest_framework import generics
from .serializers import AttributeSerializer
from eav.models import Attribute

# Create your views here.


class ProposalAttributesView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
