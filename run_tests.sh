#!/bin/bash
# run_tests.sh
# Automated test runner with logging - built with Codex assistance

LOG_DIR="logs"
mkdir -p $LOG_DIR
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/test_run_$TIMESTAMP.log"

echo "========================================" | tee -a $LOG_FILE
echo "netmon-autotest run: $TIMESTAMP" | tee -a $LOG_FILE
echo "========================================" | tee -a $LOG_FILE

# Check interfaces are reachable
echo "Checking Python environment..." | tee -a $LOG_FILE
python3 --version | tee -a $LOG_FILE

# Run pytest and log results
echo "Running pytest suite..." | tee -a $LOG_FILE
pytest test_telemetry.py -v 2>&1 | tee -a $LOG_FILE

# Check result
if [ $? -eq 0 ]; then
    echo "✅ All tests passed - $TIMESTAMP" | tee -a $LOG_FILE
else
    echo "❌ Some tests failed - check $LOG_FILE" | tee -a $LOG_FILE
fi

echo "Log saved to $LOG_FILE"
