#!/usr/bin/env python3
"""Mock network telemetry server for NetQ-style verification."""

from __future__ import annotations
import json
import random
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone

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

def introduce_anomaly(state: SwitchState) -> None:
    anomaly = random.choice([
        "cpu_spike", "interface_down", "memory_spike",
        "packet_drop_surge", "bandwidth_drop"
    ])
    state.active_anomaly = anomaly
    state.anomaly_ticks_remaining = 3
    if anomaly == "cpu_spike":
        state.cpu_utilization = random.uniform(85.0, 99.0)
    elif anomaly == "interface_down":
        iface = random.choice(list(state.interface_status))
        state.interface_status[iface] = "down"
    elif anomaly == "memory_spike":
        state.memory_usage = random.uniform(88.0, 98.0)
    elif anomaly == "packet_drop_surge":
        state.packet_drop_rate = random.uniform(2.0, 8.0)
    elif anomaly == "bandwidth_drop":
        state.network_bandwidth_mbps = random.uniform(10.0, 100.0)

def generate_telemetry(device_id: str, state: SwitchState) -> dict:
    if state.anomaly_ticks_remaining > 0:
        state.anomaly_ticks_remaining -= 1
    else:
        state.active_anomaly = None
        state.cpu_utilization = max(5.0, min(45.0, state.cpu_utilization + random.uniform(-3, 3)))
        state.memory_usage = max(25.0, min(75.0, state.memory_usage + random.uniform(-1.5, 1.5)))
        state.network_bandwidth_mbps = max(500.0, min(10000.0, state.network_bandwidth_mbps + random.uniform(-150, 150)))
        state.packet_drop_rate = max(0.0, min(0.5, state.packet_drop_rate + random.uniform(-0.005, 0.005)))
        if random.random() < 0.12:
            introduce_anomaly(state)
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
    print("Starting telemetry emission... Press Ctrl+C to stop.", flush=True)
    try:
        while True:
            payload = generate_telemetry("switch-leaf-01", state)
            print(json.dumps(payload), flush=True)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()
