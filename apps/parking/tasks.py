from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

from .models import Device, Alert
from .services.alerts import create_or_touch_alert


@shared_task
def check_device_offline():
    now = timezone.now()
    cutoff = now - timedelta(minutes=2)

    qs = Device.objects.filter(is_active=True).filter(
        Q(last_seen__lt=cutoff) | Q(last_seen__isnull=True)
    )

    created_count = 0
    touched_count = 0

    for d in qs:
        msg = f"Device {d.device_code} is offline. last_seen={d.last_seen}"
        alert, created = create_or_touch_alert(
            d, Alert.DEVICE_OFFLINE, Alert.CRITICAL, msg
        )
        if created:
            created_count += 1
        else:
            touched_count += 1

    return {"created": created_count, "touched": touched_count}
