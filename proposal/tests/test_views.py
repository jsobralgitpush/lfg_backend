from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from eav.models import Attribute
from proposal.serializers import AttributeSerializer


class ProposalAttributesViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('proposal:attributes')
        self.attribute1 = Attribute.objects.create(
            name='Attribute 1', datatype=Attribute.TYPE_TEXT)
        self.attribute2 = Attribute.objects.create(
            name='Attribute 2', datatype=Attribute.TYPE_TEXT)

    def test_get_proposal_attributes(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        serializer = AttributeSerializer(
            [self.attribute1, self.attribute2], many=True)
        self.assertEqual(response.data, serializer.data)
