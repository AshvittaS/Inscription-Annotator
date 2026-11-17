#!/bin/sh
# Start the Vatteluttu annotator on macOS / Linux. Keep this terminal open while annotating.
cd "$(dirname "$0")" || exit 1
if command -v python3 >/dev/null 2>&1; then
  exec python3 annotator_server.py
else
  exec python annotator_server.py
fi
