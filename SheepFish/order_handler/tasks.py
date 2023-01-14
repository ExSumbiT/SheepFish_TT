from django.template.loader import render_to_string
from django.core.files import File
from django.conf import settings
from .models import Check
from celery import shared_task
import json
import requests
import base64


@shared_task
def html_to_pdf(check_id):
    check = Check.objects.filter(id=check_id).first()
    context = {'check': check}
    url = 'http://localhost:8080/'
    content = render_to_string('OrderDetails.html', context)
    data = {
        'contents': base64.b64encode(bytes(content, 'utf-8')).decode(),
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)

    # Save the response contents to a file
    with open(str(settings.MEDIA_ROOT) + f'\\pdf\\{check.order["id"]}_{check.type}.pdf', 'wb') as f:
        f.write(response.content)
        check.status = 'rendered'
        check.pdf_file = f
    return True
