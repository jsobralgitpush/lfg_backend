
from loans_for_good.celery import app
from .services import send_proposal_service
from .models import Proposal


@app.task(name='proposal.tasks.send_proposal_task')
def send_proposal_task(name, document, proposal_id):
    proposal = Proposal.objects.get(id=proposal_id)
    response = send_proposal_service(name, document, proposal_id)

    if response.status_code == 200:
        proposal.status = 'pending_by_analyst' if response.json().get(
            'approved') == 'True' else 'denied'
        proposal.save()
