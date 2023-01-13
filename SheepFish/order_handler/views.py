from celery.result import AsyncResult
from .tasks import html_to_pdf
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
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
            return JsonResponse({"message": "Checks already exists for this order"}, status=400)
    return JsonResponse({"message": "ok"}, status=201)


@require_POST
@csrf_exempt
def post_order(request):
    order_json = json.loads(request.body)
    return generate_checks(order_json)


@csrf_exempt
def run_task(request):
    if request.POST:
        task_type = request.POST.get("type")
        task = create_task.delay(int(task_type))
        return JsonResponse({"task_id": task.id}, status=202)


@csrf_exempt
def get_status(request, task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JsonResponse(result, status=200)
