#!/usr/bin/env python3
"""Mock network telemetry server for NetQ-style verification."""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

DEFAULT_INTERFACES = ("swp1", "swp2", "swp3", "swp4", "mgmt0")

@dataclass
class SwitchState:
    cpu_utilization: float = 15.0
    memory_usage: float = 40.0
    network_bandwidth_mbps: float = 2500.0
    packet_drop_rate: float = 0.01
    interface_status: dict[str, str] = field(
        default_factory=lambda: {name: "up" for name in DEFAULT_INTERFACES}
    )
    active_anomaly: str | None = None
    anomaly_ticks_remaining: int = 0

def generate_telemetry(device_id: str, state: SwitchState) -> dict:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "device_id": device_id,
        "cpu_utilization": round(state.cpu_utilization, 2),
        "memory_usage": round(state.memory_usage, 2),
        "network_bandwidth_mbps": round(state.network_bandwidth_mbps, 2),
        "interface_status": dict(state.interface_status),
        "packet_drop_rate": round(state.packet_drop_rate, 4),
        "anomaly": state.active_anomaly,
    }

def main():
    state = SwitchState()
    try:
        while True:
            payload = generate_telemetry("switch-leaf-01", state)
            print(json.dumps(payload), flush=True)
            time.sleep(2)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
