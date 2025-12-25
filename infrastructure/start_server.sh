#!/bin/bash
# Start V3Di 3D Slicer Backend

cd /opt/v3di-backend
source venv/bin/activate

# Set environment variables
export SLICER_HOME=/opt/v3di-backend/Slicer
export S3_BUCKET=v3di-slicer-data
export AWS_REGION=eu-west-2

# Start with Xvfb for headless 3D rendering
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x24 &
sleep 2

# Start uvicorn
echo "Starting V3Di Backend on port 8001..."
nohup uvicorn api.main:app --host 0.0.0.0 --port 8001 > server.log 2>&1 &

echo "Backend started. Check server.log for output."
echo "Health check: curl http://localhost:8001/health"
