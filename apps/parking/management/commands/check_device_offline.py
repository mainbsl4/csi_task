from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
# from api.models import Device, Alert
# from api.services.alerts import create_or_touch_alert
from apps.parking.models import Device, Alert
from apps.parking.services.alerts import create_or_touch_alert
from django.db.models import Q

class Command(BaseCommand):
    help = "Create/Update offline alerts for devices not seen in last 2 minutes"

    def handle(self, *args, **options):
        now = timezone.now()
        cutoff = now - timedelta(minutes=2)

        qs = Device.objects.filter(is_active=True).filter(Q(last_seen__lt=cutoff) | Q(last_seen__isnull=True))

        created_count = 0
        touched_count = 0
        for d in qs:
            msg = f"Device {d.device_code} is offline. last_seen={d.last_seen}"
            alert, created = create_or_touch_alert(d, Alert.DEVICE_OFFLINE, Alert.CRITICAL, msg)
            if created:
                created_count += 1
            else:
                touched_count += 1

        self.stdout.write(self.style.SUCCESS(f"Offline check done. created={created_count} touched={touched_count}"))
