#!/bin/bash
echo "🚀 Tracker launching at $(date)" >> "$HOME/tracker_debug.log"
cd "$(dirname "$0")"
python3 -u -m finance_app.main

