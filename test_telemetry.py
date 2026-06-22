"""pytest suite for mock_server.py telemetry validation."""
from datetime import datetime
from mock_server import SwitchState, generate_telemetry, introduce_anomaly

KNOWN_ANOMALIES = {
    "cpu_spike", "interface_down", "memory_spike",
    "packet_drop_surge", "bandwidth_drop"
}

def make_payload(device_id="switch-leaf-01"):
    state = SwitchState()
    return generate_telemetry(device_id, state), state

def test_payload_has_all_fields():
    payload, _ = make_payload()
    for field in ["timestamp","device_id","cpu_utilization",
                  "memory_usage","network_bandwidth_mbps",
                  "interface_status","packet_drop_rate","anomaly"]:
        assert field in payload

def test_cpu_within_range():
    state = SwitchState()
    for _ in range(50):
        p = generate_telemetry("switch-leaf-01", state)
        assert 0 <= p["cpu_utilization"] <= 100

def test_memory_within_range():
    state = SwitchState()
    for _ in range(50):
        p = generate_telemetry("switch-leaf-01", state)
        assert 0 <= p["memory_usage"] <= 100

def test_interface_status_values():
    payload, _ = make_payload()
    for iface, status in payload["interface_status"].items():
        assert status in ("up", "down")

def test_packet_drop_not_negative():
    state = SwitchState()
    for _ in range(50):
        p = generate_telemetry("switch-leaf-01", state)
        assert p["packet_drop_rate"] >= 0

def test_timestamp_valid_iso():
    payload, _ = make_payload()
    parsed = datetime.fromisoformat(payload["timestamp"])
    assert parsed is not None

def test_device_id_correct():
    payload, _ = make_payload("switch-spine-02")
    assert payload["device_id"] == "switch-spine-02"

def test_anomaly_is_known_or_null():
    state = SwitchState()
    for _ in range(100):
        p = generate_telemetry("switch-leaf-01", state)
        assert p["anomaly"] is None or p["anomaly"] in KNOWN_ANOMALIES

def test_switchstate_defaults():
    s = SwitchState()
    assert s.cpu_utilization == 15.0
    assert s.memory_usage == 40.0
    assert s.anomaly_ticks_remaining == 0
    assert s.active_anomaly is None

def test_all_interfaces_start_up():
    s = SwitchState()
    for status in s.interface_status.values():
        assert status == "up"

def test_anomaly_injection():
    state = SwitchState()
    introduce_anomaly(state)
    assert state.active_anomaly in KNOWN_ANOMALIES
    assert state.anomaly_ticks_remaining > 0

def test_bandwidth_positive():
    state = SwitchState()
    for _ in range(50):
        p = generate_telemetry("switch-leaf-01", state)
        assert p["network_bandwidth_mbps"] > 0
