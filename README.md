# netmon-autotest

Python test automation suite for network telemetry simulation — built with Cursor AI and Codex.

## What it does

Simulates a network switch emitting real-time JSON telemetry (CPU, memory, bandwidth, interface status) with random anomaly injection. A full pytest suite validates every field, and a Bash script automates test runs with logging.

## Project structure
## Quick start

```bash
# Run the telemetry server
python3 mock_server.py

# Run tests
pytest test_telemetry.py -v

# Run automated test loop with logging
./run_tests.sh
```

## How AI tools were used

| Stage | Tool | What it did |
|-------|------|-------------|
| Before | Manual | Basic skeleton, 3 lines, no structure |
| Day 1 | Cursor AI | Generated full telemetry server with anomaly injection |
| Day 2 | Cursor AI | Scaffolded 12 pytest cases covering edge cases |
| Day 3 | Codex | Built bash automation script with logging |

## Skills demonstrated

- Python automation and test engineering
- pytest (functional, regression, edge case testing)
- Bash scripting and Linux environments
- AI-assisted development workflow (Cursor, Codex)
- Network telemetry concepts (NetQ-style)

## Tech stack

Python · pytest · Bash · Linux · Cursor AI · Codex
