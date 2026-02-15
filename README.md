# CSI Parking Monitoring API

Django REST API for parking facility, zone, device, telemetry, occupancy logs, targets, and alert monitoring.

## Tech Stack
- Python 3.13
- Django 5.2.x
- Django REST Framework
- django-filter
- Celery
- django-celery-beat
- Redis (broker/result backend)
- SQLite (default local database)

## Project Structure
- `project/` - Django settings, root URLs, Celery app
- `apps/parking/` - domain models, serializers, views, URLs, tasks, services
- `apps/parking/management/commands/check_device_offline.py` - manual offline-alert command
- `db.sqlite3` - local database

## Data Model Overview
- `ParkingFacility` -> `ParkingZone` -> `Device`
- `Telemetry` belongs to `Device` (`unique_together: device + timestamp`)
- `ParkingLog` belongs to `Device` (`unique_together: device + timestamp`)
- `ParkingTarget` belongs to `ParkingZone` (`unique_together: parking_zone + date`)
- `Alert` belongs to `Device` (active/acknowledged/resolved workflow)

## Local Setup
1. Create and activate virtual environment.
2. Install dependencies.
3. Run migrations.
4. Start API server.

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install Django djangorestframework django-filter celery django-celery-beat redis
python manage.py migrate
python manage.py runserver
```

API base URL: `http://127.0.0.1:8000/api/`

## Background Processing (Celery)
Settings use Redis:
- Broker: `redis://127.0.0.1:6379/0`
- Result backend: `redis://127.0.0.1:6379/0`

Start worker and beat:

```powershell
celery -A project worker -l info
celery -A project beat -l info
```

Manual offline check command:

```powershell
python manage.py check_device_offline
```

Offline criteria in current code: device `is_active=True` and `last_seen` older than 2 minutes (or null).

## API Endpoints
All routes are prefixed with `/api/`.

### Parking Facilities
- `GET /facilities/` - list facilities (filter: `name`)
- `POST /facilities/` - create facility
- `GET /facilities/<id>/` - facility details

### Parking Zones
- `GET /zones/` - list zones (filters: `parking_facility`, `name`, `code`)
- `POST /zones/` - create zone
- `GET /zones/<id>/` - zone details

### Devices
- `GET /devices/` - list devices (filters: `parking_zone`, `device_code`, `is_active`)
- `POST /devices/` - create device
- `GET /devices/<id>/` - device details
- `GET /devices/status/` - dashboard device status (`zone_code`, `facility_id` optional)

### Telemetry
- `GET /telemetry/` - list telemetry (filters: `device__device_code`, `voltage`, `current`, `power_factor`)
- `POST /telemetry/` - create one telemetry row
- `GET /telemetry/<id>/` - telemetry details
- `POST /telemetry/bulk/` - bulk ingest telemetry records

### Parking Logs and Targets
- `GET /parking-log/` - list logs (filters: `device__device_code`, `is_occupied`)
- `POST /parking-log/` - create log
- `GET /parking-log/<id>/` - log details
- `GET /parking-target/` - list targets
- `POST /parking-target/` - create target

### Dashboard and Metrics
- `GET /dashboard/summary/` - KPI summary
  - optional query params: `date` (`YYYY-MM-DD`), `facility`, `zone_code`
- `GET /metrics/hourly-usage/` - hourly occupancy/event aggregation
  - optional query params: `date` (`YYYY-MM-DD`), `facility_id`, `zone_code`

### Alerts
- `GET /alerts/` - list alerts (filters: `status`, `severity`, `alert_type`, `device__device_code`)
- `PATCH /alerts/<id>/ack/` - acknowledge alert
- `PATCH /alerts/<id>/resolve/` - resolve alert

## Request Examples
Create device:

```bash
curl -X POST http://127.0.0.1:8000/api/devices/ \
  -H "Content-Type: application/json" \
  -d '{
    "parking_zone": 1,
    "device_code": "PARK-B1-S005",
    "is_active": true
  }'
```

Post telemetry (single):

```bash
curl -X POST http://127.0.0.1:8000/api/telemetry/ \
  -H "Content-Type: application/json" \
  -d '{
    "device_code": "PARK-B1-S005",
    "voltage": 220.5,
    "current": 1.8,
    "power_factor": 0.93,
    "timestamp": "2026-02-15T10:15:00Z"
  }'
```

Post telemetry (bulk):

```bash
curl -X POST http://127.0.0.1:8000/api/telemetry/bulk/ \
  -H "Content-Type: application/json" \
  -d '{
    "records": [
      {
        "device_code": "PARK-B1-S005",
        "voltage": 221.0,
        "current": 1.7,
        "power_factor": 0.94,
        "timestamp": "2026-02-15T10:16:00Z"
      },
      {
        "device_code": "PARK-B1-S005",
        "voltage": 220.6,
        "current": 1.6,
        "power_factor": 0.92,
        "timestamp": "2026-02-15T10:17:00Z"
      }
    ]
  }'
```

## Notes and Current Caveats
- Many detail views currently expose only `GET` handlers in `views.py`.
- `telemetry` and `parking-log` reject timestamps too far in the future (`> now + 5 minutes`).
- `telemetry/bulk/` uses `bulk_create(ignore_conflicts=True)`, so duplicate `(device, timestamp)` rows are skipped.
- In `project/settings.py`, Celery beat schedule references `api.tasks.check_device_offline`; the task function currently exists at `apps.parking.tasks.check_device_offline`.

## Authentication and Permissions
- Most endpoints use `AllowAny` in current implementation.
- Global DRF default is `DjangoModelPermissionsOrAnonReadOnly`, but per-view `AllowAny` overrides this where declared.

## CORS (Frontend Access)
Current status:
- `django-cors-headers` is not configured in `project/settings.py`.
- If your frontend runs on a different origin (example: `http://localhost:5173`), browser requests to this API can fail due to CORS.

Recommended setup:
1. Install package:

```powershell
pip install django-cors-headers
```

2. Update `INSTALLED_APPS` in `project/settings.py`:

```python
INSTALLED_APPS = [
    # ...
    "corsheaders",
    # ...
]
```

3. Add middleware near the top (before `CommonMiddleware`):

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # ...
]
```

4. Allow only trusted frontend origins:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
]
```

Optional (if you use cookies/session auth from frontend):

```python
CORS_ALLOW_CREDENTIALS = True
```

Production note:
- Avoid `CORS_ALLOW_ALL_ORIGINS = True` in production.
- Keep the origin list explicit per environment.

## Useful Commands
```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py check_device_offline
```
