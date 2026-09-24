# Read-only modernization bridge

The intended bridge is:

Legacy C/C++ → Adapter → REST API → Modern React dashboard

The first demo exposes only a read-only machine-status endpoint.

Suggested endpoint:

GET /api/v1/machines/{id}/status

Example response:

```json
{
  "machine_id": 7,
  "alarm_active": true,
  "production_enabled": false,
  "reason": "temperature limit exceeded",
  "source": "AUTOFACTORY-2005"
}
```

The adapter must not provide endpoints that disable alarms, start production,
stop production, or bypass safety interlocks.