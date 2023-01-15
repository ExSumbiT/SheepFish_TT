from .tasks import html_to_pdf
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from .models import Printer, Check
import json


def create_check(printer: Printer, data):
    exists = Check.objects.filter(
        printer_id=printer).filter(order__id=data['id']).exists()
    if exists:
        raise ValueError
    c = Check.objects.create(
        printer_id=printer, type=printer.check_type, order=data, status='new')
    html_to_pdf.delay(c.id)


def generate_checks(data):
    printers = Printer.objects.filter(point_id=data['point_id'])
    if not printers:
        return JsonResponse({"message": "No printers found for this point"}, status=400)
    for printer in printers:
        try:
            create_check(printer, data)
        except ValueError:
            return JsonResponse({"message": "Checks already exist for this order"}, status=400)
    return JsonResponse({"message": "ok"}, status=201)


def get_checks_for_printer(api_key):
    checks = []
    for check in Check.objects.filter(printer_id__api_key=api_key).filter(status='rendered'):
        checks.append(check.to_json())
    return JsonResponse(checks, safe=False)


@require_POST
@csrf_exempt
def post_order(request):
    order_json = json.loads(request.body)
    return generate_checks(order_json)


@require_GET
@csrf_exempt
def get_checks(request, key):
    return get_checks_for_printer(key)


@require_POST
@csrf_exempt
def print_check(request, number):
    check = Check.objects.filter(id=number).first()
    check.status = 'printed'
    check.save()
    return JsonResponse({'message': 'ok'}, status=200)
