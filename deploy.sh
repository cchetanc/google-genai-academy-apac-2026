#!/bin/bash
set -e

echo "================================================"
echo " Campus Placement Assistant v2 — Deploy Script"
echo "================================================"

# Load environment
if [ ! -f .env ]; then
  echo "ERROR: .env not found. Run setup/setup_env.sh first."
  exit 1
fi
source .env
echo "Deploying to project: $PROJECT_ID, region: $REGION"

# Deploy to Cloud Run via ADK
echo ""
echo ">>> Deploying to Cloud Run..."
uvx --from google-adk==1.14.0 \
  adk deploy cloud_run \
  --project=$PROJECT_ID \
  --region=$REGION \
  --service_name=placement-assistant-v2 \
  --with_ui \
  . \
  -- \
  --labels=track=track2,app=placement-assistant \
  --service-account=$SERVICE_ACCOUNT \
  --set-env-vars="MODEL=gemini-2.5-flash,GOOGLE_CLOUD_PROJECT=$PROJECT_ID"

echo ""
echo "================================================"
echo " Deployment complete!"
echo " Your Cloud Run URL is shown above."
echo "================================================"
