from django.db import models

check_types = (
    ('kitchen', 'Kitchen'), ('client', 'Client'))


class Printer(models.Model):
    name = models.CharField(max_length=100)
    api_key = models.CharField(max_length=50, unique=True)
    check_type = models.CharField(max_length=8, choices=check_types)
    point_id = models.IntegerField()


class Check(models.Model):
    printer_id = models.ForeignKey('Printer', on_delete=models.CASCADE)
    type = models.CharField(max_length=8, choices=check_types)
    order = models.JSONField()
    status = models.CharField(max_length=8, choices=(
        ('new', 'New'), ('rendered', 'Rendered'), ('printed', 'Printed')))
    pdf_file = models.FileField()
