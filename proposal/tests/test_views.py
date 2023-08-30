from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from eav.models import Attribute
from proposal.serializers import AttributeSerializer
from proposal.models import Proposal


class ProposalAttributesViewTestCase(APITestCase):
    def setUp(self):
        self.attribute1 = Attribute.objects.create(
            name='city', datatype=Attribute.TYPE_TEXT)
        self.attribute2 = Attribute.objects.create(
            name='address', datatype=Attribute.TYPE_TEXT)
        Proposal.objects.create(name="Proposal 1", document="Document 1")
        Proposal.objects.create(name="Proposal 2", document="Document 2")

    def test_list_proposal_attributes(self):
        """
        Ensure we can list all attributes.
        """
        url = reverse('proposal:attributes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_proposal(self):
        """
        Ensure we can create a new proposal object.
        """
        data = {'name': 'Test Name',
                'document': 'Test Document', 'city': 'TestValue'}
        url = reverse('proposal:list-create')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Proposal.objects.count(), 3)

    def test_proposal_list(self):
        """
        Ensure we can list all proposals.
        """
        url = reverse('proposal:list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'Proposal 1')
        self.assertEqual(response.data[1]['name'], 'Proposal 2')

    def test_retrieve_proposal(self):
        """
        Ensure we can retrieve a proposal.
        """
        proposal = Proposal.objects.create(
            name='Test Name', document='Test Document')
        url = reverse('proposal:retrieve', args=[proposal.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Name')
