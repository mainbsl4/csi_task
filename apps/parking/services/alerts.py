from django.utils import timezone
from ..models import Alert

def create_or_touch_alert(device, alert_type, severity, message):
    """
    If same (device, alert_type) is ACTIVE already -> touch last_triggered_at + message
    else create new ACTIVE alert
    """
    now = timezone.now()
    alert = Alert.objects.filter(
        device=device,
        alert_type=alert_type,
        status=Alert.ACTIVE
    ).first()

    if alert:
        alert.severity = severity
        alert.message = message
        alert.last_triggered_at = now
        alert.save(update_fields=["severity", "message", "last_triggered_at", "updated_at"])
        return alert, False

    alert = Alert.objects.create(
        device=device,
        alert_type=alert_type,
        severity=severity,
        status=Alert.ACTIVE,
        message=message,
        first_triggered_at=now,
        last_triggered_at=now,
    )
    return alert, True
