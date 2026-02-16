from rest_framework import serializers
from django.utils import timezone
from django.db import transaction
from .models import (
    ParkingFacility,
    ParkingZone,
    Device,
    Telemetry,
    ParkingLog,
    ParkingTarget,
    Alert,
)


# parking facility serializer
class ParkingFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingFacility
        fields = [
            "id",
            "name",
            "location",
            "created_at",
            "updated_at",
        ]


# parking zone serializer
class ParkingZoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParkingZone
        fields = [
            "id",
            "parking_facility",
            "name",
            "code",
            "created_at",
            "updated_at",
        ]


# device serializer
class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = [
            "id",
            "parking_zone",
            "device_code",
            "is_active",
            "last_seen",
            "created_at",
            "updated_at",
        ]


# telemetry serializer
class TelemetrySerializer(serializers.ModelSerializer):

    device_code = serializers.SlugRelatedField(
        queryset=Device.objects.all(), slug_field="device_code", source="device"
    )

    class Meta:
        model = Telemetry
        fields = [
            "id",
            # "device",
            "device_code",
            "voltage",
            "current",
            "power_factor",
            "timestamp",
            "created_at",
            "updated_at",
        ]

    def validate_timestamp(self, value):
        if value > timezone.now() + timezone.timedelta(minutes=5):
            raise serializers.ValidationError(
                "Invalid timestamp (too far in the future)."
            )
        return value


# Telemetry bulk serializer


class TelemetryBulkSerializer(serializers.Serializer):
    records = TelemetrySerializer(many=True, write_only=True)

    def create(self, validated_data):
        records = validated_data["records"]

        objs = []
        for rec in records:
            objs.append(
                Telemetry(
                    device=rec["device"],
                    voltage=rec["voltage"],
                    current=rec["current"],
                    power_factor=rec["power_factor"],
                    timestamp=rec["timestamp"],
                )
            )

        with transaction.atomic():
            created = Telemetry.objects.bulk_create(objs, ignore_conflicts=True)

        device_ids = list({o.device_id for o in objs})
        now = timezone.now()
        Device.objects.filter(id__in=device_ids).update(last_seen=now)

        return {
            "inserted": len(created),
            "received": len(objs),
            "skipped": len(objs) - len(created),
        }


# parking log serializer
class ParkingLogSerializer(serializers.ModelSerializer):

    device_code = serializers.SlugRelatedField(
        queryset=Device.objects.all(), slug_field="device_code", source="device"
    )

    class Meta:
        model = ParkingLog
        fields = [
            "id",
            "device_code",
            "is_occupied",
            "timestamp",
            "created_at",
            "updated_at",
        ]

    def validate_timestamp(self, value):
        if value > timezone.now() + timezone.timedelta(minutes=5):
            raise serializers.ValidationError(
                "Invalid timestamp (too far in the future)."
            )
        return value


# parking target serializer
class ParkingTargetSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParkingTarget
        fields = [
            "id",
            "parking_zone",
            "date",
            "target_parking_events",
            "created_at",
            "updated_at",
        ]


# alert serializer
class AlertSerializer(serializers.ModelSerializer):
    device_code = serializers.SlugRelatedField(
        queryset=Device.objects.all(), slug_field="device_code", source="device"
    )

    class Meta:
        model = Alert
        fields = [
            "id",
            "device_code",
            "alert_type",
            "severity",
            "status",
            "message",
            "first_triggered_at",
            "last_triggered_at",
            "created_at",
            "updated_at",
        ]
