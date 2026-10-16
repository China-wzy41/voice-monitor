"""Hardware-free sensor simulator for the first project milestone."""

import json
import math
import random
import time
from datetime import datetime, timezone
from urllib.request import Request, urlopen


API_URL = "http://127.0.0.1:8000/api/readings"


def make_reading(step: int) -> dict:
    # A repeatable daily-like wave plus small random variation.
    wave = 0.18 * math.sin(step / 8)
    value = max(0.0, min(1.0, 0.45 + wave + random.uniform(-0.04, 0.04)))
    return {
        "device_id": "room-sim-01",
        "location_id": "dorm-room",
        "metric": "noise_relative",
        "value": round(value, 4),
        "unit": "rms_normalized",
        "quality": "ok",
        "measured_at": datetime.now(timezone.utc).isoformat(),
    }


def main() -> None:
    step = 0
    while True:
        payload = json.dumps(make_reading(step)).encode("utf-8")
        request = Request(API_URL, data=payload, headers={"Content-Type": "application/json"})
        try:
            with urlopen(request, timeout=5) as response:
                print(response.status, payload.decode("utf-8"), flush=True)
        except Exception as exc:
            print("upload failed:", exc, flush=True)
        step += 1
        time.sleep(5)


if __name__ == "__main__":
    main()

