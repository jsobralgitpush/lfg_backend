import unittest
from unittest.mock import patch, Mock
from proposal.tasks import send_proposal_task


class TestSendProposalTask(unittest.TestCase):

    @patch('proposal.tasks.Proposal.objects.get')
    @patch('proposal.tasks.send_proposal_service')
    def test_successful_proposal_approved(self, mock_service, mock_get):
        """
        Test that the proposal status is updated to pending_by_analyst
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'approved': 'True'}
        mock_service.return_value = mock_response

        mock_proposal = Mock()
        mock_proposal.status = None
        mock_get.return_value = mock_proposal

        send_proposal_task('John Doe', '123456789', '12345')

        self.assertEqual(mock_proposal.status, 'pending_by_analyst')
        mock_proposal.save.assert_called_once()

    @patch('proposal.tasks.Proposal.objects.get')
    @patch('proposal.tasks.send_proposal_service')
    def test_successful_proposal_denied(self, mock_service, mock_get):
        """
        Test that the proposal status is updated to denied
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'approved': 'False'}
        mock_service.return_value = mock_response

        mock_proposal = Mock()
        mock_proposal.status = None
        mock_get.return_value = mock_proposal

        send_proposal_task('John Doe', '123456789', '12345')

        self.assertEqual(mock_proposal.status, 'denied')
        mock_proposal.save.assert_called_once()


if __name__ == '__main__':
    unittest.main()
