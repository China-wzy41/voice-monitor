# Data contract

Every sensor reading uses one record shape so future temperature, humidity, and occupancy sensors can be added without redesigning the database.

| Field | Type | Meaning |
|---|---|---|
| `device_id` | string | Physical or simulated device identifier |
| `location_id` | string | Room, zone, or seat identifier |
| `metric` | string | `noise_relative`, later `temperature`, `humidity`, etc. |
| `value` | number | Numeric reading |
| `unit` | string | Unit or representation of the value |
| `quality` | string | `ok`, `stale`, `invalid`, or `offline` |
| `measured_at` | ISO 8601 time | Time at the sensor |

The API should also record `received_at` on the server. A missing or old reading must be represented as unknown rather than silently treated as quiet or unoccupied.

