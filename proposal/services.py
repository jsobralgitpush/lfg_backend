import requests


def send_proposal_service(name, document, proposal_id):
    api_url = "https://loan-processor.digitalsys.com.br/api/v1/loan"
    response = requests.post(api_url, json={
        'name': name,
        'document': document
    })

    return response
