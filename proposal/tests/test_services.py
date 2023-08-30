import unittest
from unittest.mock import patch
import requests
from proposal.services import send_proposal_service


class TestSendProposalService(unittest.TestCase):

    @patch('requests.post')
    def test_successful_api_call(self, mock_post):
        """
        Test that the API call returns a 200 status code and a success message
        """
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'status': 'success'}

        response = send_proposal_service('John Doe', '123456789', '12345')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})

    @patch('requests.post')
    def test_api_error_response(self, mock_post):
        """
        Test that the API call returns a 400 status code and an error message
        """
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {
            'status': 'error', 'message': 'Invalid data'}

        response = send_proposal_service(
            'John Doe', 'invalid_document', '12345')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
                         'status': 'error', 'message': 'Invalid data'})

    @patch('requests.post')
    def test_request_payload(self, mock_post):
        """
        Test that the payload is structured correctly
        """
        send_proposal_service('John Doe', '123456789', '12345')

        # Check that the payload was structured correctly
        mock_post.assert_called_once_with(
            "https://loan-processor.digitalsys.com.br/api/v1/loan",
            json={'name': 'John Doe', 'document': '123456789'}
        )

    @patch('requests.post')
    def test_network_exception(self, mock_post):
        """
        Test that the API call raises an exception when there is a network error
        """
        mock_post.side_effect = requests.exceptions.RequestException

        with self.assertRaises(requests.exceptions.RequestException):
            send_proposal_service('John Doe', '123456789', '12345')


if __name__ == '__main__':
    unittest.main()
