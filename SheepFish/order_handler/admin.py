from django.contrib import admin
from .models import Printer, Check


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper


class CheckAdmin(admin.ModelAdmin):
    list_filter = [
        ("printer_id", custom_titled_filter('принтером')),
        ("type", custom_titled_filter('типом')),
        ("status", custom_titled_filter('статусом'))
    ]
    search_fields = (
        "type",
        "status",
    )


admin.site.register(Check, CheckAdmin)
admin.site.register(Printer)
# admin.site.register(Check)
