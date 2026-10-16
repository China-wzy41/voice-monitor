# Library IoT noise monitor

This project starts as a hardware-free prototype. A simulator sends noise readings to a local API so the database and web interface can be built before the ESP32 arrives.

## First milestone

- one virtual device: `room-sim-01`
- one metric: `noise_relative`
- readings stored with device ID, location, value, unit, quality, and timestamps
- API endpoints for upload, latest reading, and history

When the ESP32 is ready, it should send the same JSON shape as the simulator:

```json
{
  "device_id": "room-01",
  "location_id": "dorm-room",
  "metric": "noise_relative",
  "value": 0.42,
  "unit": "rms_normalized",
  "quality": "ok",
  "measured_at": "2026-10-16T12:00:00Z"
}
```

The value is deliberately a relative level for now. It must not be presented as calibrated dB(A) until the microphone is tested against a reference sound-level meter.

## Suggested next step

Create a Python virtual environment, install FastAPI and Uvicorn, then implement the API in `backend/main.py`. The ESP32 will later replace `simulator.py` as the data producer.

