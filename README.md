# netmon-autotest

A Python test automation suite that simulates network switch telemetry and validates it using pytest.

## Why I built this

I wanted to practice test engineering on a realistic backend scenario — specifically simulating the kind of telemetry data that network monitoring systems produce. This combined my interest in networking (CCNA concepts) with Python automation and testing.

## What it does

- Simulates a network switch emitting real-time JSON telemetry (CPU, memory, bandwidth, interface status)
- Injects random anomalies to test edge case handling
- Validates every field and data type using a pytest suite (12 test cases)
- Automates repeated test runs with logging via a Bash script

## Project structure

```
netmon-autotest/
├── mock_server.py      # Simulates a network switch emitting JSON telemetry
├── test_telemetry.py   # pytest suite — 12 test cases covering fields, types, anomalies
├── run_tests.sh        # Bash script to automate test loops with logging
└── logs/               # Test run output logs
```

## How to run

```bash
# Start the telemetry server
python3 mock_server.py

# Run the test suite
pytest test_telemetry.py -v

# Run automated test loop with logging
./run_tests.sh
```

## Skills demonstrated

- Python automation and test engineering
- pytest — functional, regression, and edge case testing
- Bash scripting in a Linux environment
- Network telemetry concepts (CPU, memory, bandwidth, interface status)
- Anomaly detection validation

## Tech stack

Python · pytest · Bash · Linux

---

*AI coding tools were used as productivity aids during development.*
