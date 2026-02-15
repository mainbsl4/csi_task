from rest_framework import mixins
from rest_framework import generics
from .models import (
    ParkingFacility,
    ParkingZone,
    Device,
    Telemetry,
    ParkingLog,
    ParkingTarget,
    Alert,
)
from .serializer import (
    ParkingFacilitySerializer,
    ParkingZoneSerializer,
    DeviceSerializer,
    TelemetrySerializer,
    TelemetryBulkSerializer,
    ParkingLogSerializer,
    ParkingTargetSerializer,
    AlertSerializer,
)
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Max, Q, Sum
from django.utils import timezone

from datetime import datetime, time, timedelta
from django.utils.dateparse import parse_date
from django.db.models.functions import TruncHour


# -------------------parking facility views-------------------
# parking facility views
class ParkingFacilityList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = ParkingFacility.objects.all()
    serializer_class = ParkingFacilitySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# parking facility detail views
class ParkingFacilityDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = ParkingFacility.objects.all()
    serializer_class = ParkingFacilitySerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# -------------------parking zone views-------------------
# parking zone views
class ParkingZoneList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = ParkingZone.objects.all()
    serializer_class = ParkingZoneSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["parking_facility", "name", "code"]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# parking zone detail views
class ParkingZoneDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = ParkingZone.objects.all()
    serializer_class = ParkingZoneSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# -------------------device views-------------------
# device views
class DeviceList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["parking_zone", "device_code", "is_active"]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# device detail views
class DeviceDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# -------------------telemetry views-------------------
# telemetry views
class TelemetryList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Telemetry.objects.all()
    serializer_class = TelemetrySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["device__device_code", "voltage", "current", "power_factor"]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TelemetryDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Telemetry.objects.all()
    serializer_class = TelemetrySerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# -------------------bulk telemetry views-------------------
# bulk telemetry views
class BulkTelemetryList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Telemetry.objects.all()
    serializer_class = TelemetryBulkSerializer
    permission_classes = [AllowAny]

    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# -------------------parking log views-------------------
# parking log views
class ParkingLogList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = ParkingLog.objects.all()
    serializer_class = ParkingLogSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["device__device_code", "is_occupied"]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# parking log detail views
class ParkingLogDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = ParkingLog.objects.all()
    serializer_class = ParkingLogSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


#  parking target list
class ParkingTargetList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = ParkingTarget.objects.all()
    serializer_class = ParkingTargetSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DashboardSummaryList(APIView):
    permission_classes = [AllowAny]

    def _date_bounds(self, date_str: str):
        d = parse_date(date_str)
        if not d:
            return None, None, "Invalid date. Use YYYY-MM-DD."
        start = timezone.make_aware(datetime.combine(d, time.min))
        end = timezone.make_aware(datetime.combine(d, time.max))
        return start, end, None

    def get(self, request, format=None):
        date_str = request.query_params.get("date")  # optional
        facility_id = request.query_params.get("facility")  # optional
        zone_code = request.query_params.get("zone_code")  # optional

        logs_qs = ParkingLog.objects.all()
        devices_qs = Device.objects.all()
        zones_qs = ParkingZone.objects.all()

        # ----------------------------
        # Optional filters
        # ----------------------------
        if date_str:
            start_dt, end_dt, err = self._date_bounds(date_str)
            if err:
                return Response({"detail": err}, status=400)
            logs_qs = logs_qs.filter(timestamp__range=(start_dt, end_dt))

        if facility_id:
            logs_qs = logs_qs.filter(
                device__parking_zone__parking_facility_id=facility_id
            )
            devices_qs = devices_qs.filter(
                parking_zone__parking_facility_id=facility_id
            )
            zones_qs = zones_qs.filter(parking_facility_id=facility_id)

        if zone_code:
            logs_qs = logs_qs.filter(device__parking_zone__code=zone_code)
            devices_qs = devices_qs.filter(parking_zone__code=zone_code)
            zones_qs = zones_qs.filter(code=zone_code)

        # ----------------------------
        # Top-level KPIs
        # ----------------------------
        total_parking_events = logs_qs.count()

        active_devices_count = devices_qs.filter(is_active=True).count()

        # Current occupancy = latest log per device in the filtered logs_qs
        latest_by_device = logs_qs.values("device_id").annotate(
            last_ts=Max("timestamp")
        )
        pairs = [
            (r["device_id"], r["last_ts"])
            for r in latest_by_device
            if r["last_ts"] is not None
        ]

        current_occupied_devices = 0
        if pairs:
            q = Q()
            for device_id, ts in pairs:
                q |= Q(device_id=device_id, timestamp=ts)
            latest_rows = ParkingLog.objects.filter(q)
            current_occupied_devices = latest_rows.filter(is_occupied=True).count()

        # alerts_triggered_count: ideally Alert table থেকে; আপাতত placeholder বা ParkingLog based নয়
        alerts_triggered_count = 0

        # Target + efficiency (only meaningful when date exists and ParkingTarget exists)
        target_total = None
        efficiency = None
        if date_str and ParkingTarget is not None:
            target_total = (
                ParkingTarget.objects.filter(date=date_str)
                .filter(parking_zone__in=zones_qs)
                .aggregate(total=Sum("target_parking_events"))["total"]
            ) or 0
            if target_total > 0:
                efficiency = round((total_parking_events / target_total) * 100, 2)
        else:
            # no date => target doesn't make sense; keep None
            target_total = None
            efficiency = None

        # ----------------------------
        # Zone-wise indicators (only zones in filtered scope)
        # ----------------------------
        zone_wise_indicators = {}
        for zone in zones_qs:
            zone_logs = logs_qs.filter(device__parking_zone=zone)

            zone_total = zone_logs.count()

            z_latest = zone_logs.values("device_id").annotate(last_ts=Max("timestamp"))
            z_pairs = [
                (r["device_id"], r["last_ts"])
                for r in z_latest
                if r["last_ts"] is not None
            ]

            zone_current_occ = 0
            if z_pairs:
                zq = Q()
                for did, ts in z_pairs:
                    zq |= Q(device_id=did, timestamp=ts)
                z_latest_rows = ParkingLog.objects.filter(zq)
                zone_current_occ = z_latest_rows.filter(is_occupied=True).count()

            zone_target = None
            zone_eff = None
            if date_str and ParkingTarget is not None:
                zone_target = (
                    ParkingTarget.objects.filter(date=date_str, parking_zone=zone)
                    .values_list("target_parking_events", flat=True)
                    .first()
                )
                if zone_target and zone_target > 0:
                    zone_eff = round((zone_total / zone_target) * 100, 2)

            zone_wise_indicators[zone.code] = {
                "total_parking_events": zone_total,
                "current_occupancy_count": zone_current_occ,
                "active_devices_count": devices_qs.filter(
                    parking_zone=zone, is_active=True
                ).count(),
                "alerts_triggered_count": 0,  # later from Alert model
                "target_parking_events": zone_target,
                "efficiency": zone_eff,
            }

        return Response(
            {
                # "filters": {
                #     "date": date_str,
                #     "facility": facility_id,
                #     "zone_code": zone_code,
                # },
                "total_parking_events": total_parking_events,
                "current_occupancy_count": current_occupied_devices,
                "active_devices_count": active_devices_count,
                "alerts_triggered_count": alerts_triggered_count,
                "target_parking_events": target_total,
                "efficiency": efficiency,
                "zone_wise_indicators": zone_wise_indicators,
            },
            status=status.HTTP_200_OK,
        )


# hourly usage view


class HourlyUsageView(APIView):
    permission_classes = [AllowAny]

    def _date_bounds(self, date_str: str):
        d = parse_date(date_str)
        if not d:
            return None, None, "Invalid date. Use YYYY-MM-DD."
        start = timezone.make_aware(datetime.combine(d, time.min))
        end = timezone.make_aware(datetime.combine(d, time.max))
        return start, end, None

    def get(self, request):
        date_str = request.query_params.get("date")  # optional
        facility_id = request.query_params.get("facility_id")  # optional
        zone_code = request.query_params.get("zone_code")  # optional

        qs = ParkingLog.objects.all()

        # ---- optional date filter ----
        if date_str:
            start_dt, end_dt, err = self._date_bounds(date_str)
            if err:
                return Response({"detail": err}, status=400)
            qs = qs.filter(timestamp__range=(start_dt, end_dt))

        # ---- optional facility filter ----
        if facility_id:
            qs = qs.filter(device__parking_zone__parking_facility_id=facility_id)

        # ---- optional zone filter ----
        if zone_code:
            qs = qs.filter(device__parking_zone__code=zone_code)

        data = (
            qs.annotate(hour=TruncHour("timestamp"))
            .values("hour")
            .annotate(
                total_events=Count("id"),
                occupied_events=Count("id", filter=Q(is_occupied=True)),
            )
            .order_by("hour")
        )

        return Response(
            {
                "hourly": list(data),
            }
        )


# -------------------alert views-------------------


class AlertList(generics.ListAPIView):
    queryset = Alert.objects.all().order_by("-last_triggered_at")
    serializer_class = AlertSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "severity", "alert_type", "device__device_code"]


class AlertAcknowledgeView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, pk):
        alert = Alert.objects.get(pk=pk)
        alert.status = Alert.ACK
        alert.save(update_fields=["status", "updated_at"])
        return Response(AlertSerializer(alert).data)


class AlertResolveView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, pk):
        alert = Alert.objects.get(pk=pk)
        alert.status = Alert.RESOLVED
        alert.save(update_fields=["status", "updated_at"])
        return Response(AlertSerializer(alert).data)


# device status view (for dashboard)


class DeviceStatusView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        zone_code = request.query_params.get("zone_code")
        facility_id = request.query_params.get("facility")

        qs = Device.objects.select_related(
            "parking_zone", "parking_zone__parking_facility"
        )

        if zone_code:
            qs = qs.filter(parking_zone__code=zone_code)
        if facility_id:
            qs = qs.filter(parking_zone__parking_facility_id=facility_id)

        now = timezone.now()
        offline_cutoff = now - timedelta(minutes=2)

        # annotate active alert count
        qs = qs.annotate(
            active_alerts=Count("alerts", filter=Q(alerts__status=Alert.ACTIVE))
        )

        out = []
        for d in qs:
            # status
            if not d.last_seen or d.last_seen < offline_cutoff:
                status_label = "OFFLINE"
            elif d.active_alerts > 0:
                status_label = "ALERT"
            else:
                status_label = "OK"

            score = 0
            if d.last_seen and d.last_seen >= offline_cutoff:
                score += 60
            if d.is_active:
                score += 20
            # penalty for active alerts
            score -= min(d.active_alerts * 10, 30)
            score = max(0, min(100, score))

            out.append(
                {
                    "device_code": d.device_code,
                    "zone_code": d.parking_zone.code,
                    "facility": d.parking_zone.parking_facility.name,
                    "is_active": d.is_active,
                    "last_seen": d.last_seen,
                    "status": status_label,
                    "health_score": score,
                    "active_alerts": d.active_alerts,
                }
            )

        return Response({"results": out})
