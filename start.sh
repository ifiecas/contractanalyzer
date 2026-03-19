#!/bin/bash

echo "🚀 Starting Contract Analyzer..."
echo ""
echo "🤖 Loading Phi-4-mini..."
foundry model run phi-4-mini &
FOUNDRY_PID=$!

sleep 10

echo "🌐 Starting app..."
cd /Users/ifiecas/contract-analyzer
source venv/bin/activate
streamlit run app.py

kill $FOUNDRY_PID
echo "👋 Shutting down..."