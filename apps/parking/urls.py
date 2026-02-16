from django.urls import path
from .views import (
    ParkingFacilityList,
    ParkingFacilityDetail,
    ParkingZoneList,
    ParkingZoneDetail,
    DeviceList,
    DeviceDetail,
    TelemetryList,
    TelemetryDetail,
    BulkTelemetryList,
    ParkingLogList,
    ParkingLogDetail,
    ParkingTargetList,
    DashboardSummaryList,
    HourlyUsageView,
    AlertList,
    AlertAcknowledgeView,
    AlertResolveView,
    DeviceStatusView,
)

urlpatterns = [
    # parking facility urls
    path("facilities/", ParkingFacilityList.as_view(), name="parking-facility-list"),
    path(
        "facilities/<int:pk>/",
        ParkingFacilityDetail.as_view(),
        name="parking-facility-detail",
    ),
    # parking zone urls
    path("zones/", ParkingZoneList.as_view(), name="parking-zone-list"),
    path("zones/<int:pk>/", ParkingZoneDetail.as_view(), name="parking-zone-detail"),
    # device urls
    path("devices/", DeviceList.as_view(), name="device-list"),
    path("devices/<int:pk>/", DeviceDetail.as_view(), name="device-detail"),
    # telemetry urls
    path("telemetry/", TelemetryList.as_view(), name="telemetry-list"),
    path("telemetry/<int:pk>/", TelemetryDetail.as_view(), name="telemetry-detail"),
    # bulk telemetry urls
    path("telemetry/bulk/", BulkTelemetryList.as_view(), name="bulk-telemetry-list"),
    # parking urls
    path("parking-log/", ParkingLogList.as_view(), name="parking-log-list"),
    path(
        "parking-log/<int:pk>/", ParkingLogDetail.as_view(), name="parking-log-detail"
    ),
    path("parking-target/", ParkingTargetList.as_view(), name="parking-target-list"),
    # dashboard urls
    path(
        "dashboard/summary/", DashboardSummaryList.as_view(), name="dashboard-summary"
    ),
    path("metrics/hourly-usage/", HourlyUsageView.as_view(), name="hourly-usage"),
    path("alerts/", AlertList.as_view(), name="alert-list"),
    path("alerts/<int:pk>/ack/", AlertAcknowledgeView.as_view(), name="alert-ack"),
    path("alerts/<int:pk>/resolve/", AlertResolveView.as_view(), name="alert-resolve"),
    path("devices/status/", DeviceStatusView.as_view(), name="device-status"),
]
