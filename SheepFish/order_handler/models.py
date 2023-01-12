from django.db import models

check_types = (
    ('kitchen', 'Kitchen'), ('client', 'Client'))


class Printer(models.Model):
    name = models.CharField()
    api_key = models.CharField(primary_key=True)
    check_type = models.CharField(max_length=8, choices=check_types)
    point_id = models.IntegerField()


class Check(models.Model):
    printer_id = models.ForeignKey()
    type = models.CharField(max_length=8, choices=check_types)
    order = models.JSONField()
    status = models.CharField(max_length=8, choices=(
        ('new', 'New'), ('rendered', 'Rendered'), ('printed', 'Printed')))
    pdf_file = models.FileField()
