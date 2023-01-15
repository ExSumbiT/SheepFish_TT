from django.template.loader import render_to_string
from django.core.files import File
from django.conf import settings
from .models import Check
from celery import shared_task
import json
import requests
import base64
import io


@shared_task
def html_to_pdf(check_id):
    check = Check.objects.filter(id=check_id).first()
    total_price = 0
    dishes = check.order['info'].copy()
    for dish in dishes:
        dish['total'] = round(dish['price'] * dish['number'], 2)
        total_price += dish['total']
    context = {'check': check, 'total_price': round(
        total_price, 2), 'dishes': dishes}
    url = 'http://localhost:8080/'
    content = render_to_string('OrderDetails.html', context)
    data = {
        'contents': base64.b64encode(bytes(content, 'utf-8')).decode(),
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)

    # Save the response contents to a file

    check.pdf_file = File(io.BytesIO(response.content),
                          name=f"{check.order['id']}_{check.type}.pdf")
    check.status = 'rendered'
    check.save()
    return True
