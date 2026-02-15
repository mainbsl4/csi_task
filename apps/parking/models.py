from django.db import models
from django.utils import timezone

# Create your models here.


class ParkingFacility(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ParkingZone(models.Model):
    parking_facility = models.ForeignKey(
        ParkingFacility, on_delete=models.CASCADE, related_name="parking_zones"
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.parking_facility.name} - {self.name}"


class Device(models.Model):
    parking_zone = models.ForeignKey(
        ParkingZone, on_delete=models.CASCADE, related_name="devices"
    )
    device_code = models.CharField(max_length=100, unique=True)  # PARK-B1-S005
    is_active = models.BooleanField(default=True)
    last_seen = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.parking_zone.code} - {self.device_code}"


class Telemetry(models.Model):
    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, related_name="telemetries"
    )
    voltage = models.FloatField()
    current = models.FloatField()
    power_factor = models.FloatField()
    timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("device", "timestamp")

    def __str__(self):
        return f"{self.device.device_code} - {self.timestamp}"


class ParkingLog(models.Model):
    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, related_name="parking_logs"
    )
    is_occupied = models.BooleanField()
    timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("device", "timestamp")

    def __str__(self):
        return f"{self.device.device_code} - {self.is_occupied} @ {self.timestamp}"



class ParkingTarget(models.Model):
    parking_zone = models.ForeignKey(
        ParkingZone, on_delete=models.CASCADE, related_name="targets"
    )
    date = models.DateField()
    target_parking_events = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("parking_zone", "date")

    def __str__(self):
        return f"{self.parking_zone.code} {self.date} target={self.target_parking_events}"



class Alert(models.Model):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    SEVERITY_CHOICES = [(INFO, "Info"), (WARNING, "Warning"), (CRITICAL, "Critical")]

    DEVICE_OFFLINE = "DEVICE_OFFLINE"
    HIGH_POWER = "HIGH_POWER"
    INVALID_DATA = "INVALID_DATA"
    ALERT_TYPE_CHOICES = [
        (DEVICE_OFFLINE, "Device Offline"),
        (HIGH_POWER, "High Power Usage"),
        (INVALID_DATA, "Invalid Data"),
    ]

    ACTIVE = "ACTIVE"
    ACK = "ACKNOWLEDGED"
    RESOLVED = "RESOLVED"
    STATUS_CHOICES = [(ACTIVE, "Active"), (ACK, "Acknowledged"), (RESOLVED, "Resolved")]

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="alerts")
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPE_CHOICES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ACTIVE)
    message = models.TextField()

    first_triggered_at = models.DateTimeField(default=timezone.now)
    last_triggered_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.device.device_code} - {self.alert_type} ({self.severity}) - {self.status}"