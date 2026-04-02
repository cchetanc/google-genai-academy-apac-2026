#!/bin/bash
set -e

echo "================================================"
echo " Campus Placement Assistant v2 — Setup Script"
echo "================================================"

PROJECT_ID=$(gcloud config get-value project)
REGION="asia-south1"
USER_EMAIL=$(gcloud auth list --filter=status:ACTIVE --format="value(account)")

echo "Project : $PROJECT_ID"
echo "Region  : $REGION"
echo "User    : $USER_EMAIL"
echo ""

# Enable APIs
echo ">>> Enabling required GCP APIs..."
gcloud services enable \
  aiplatform.googleapis.com \
  firestore.googleapis.com \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  logging.googleapis.com \
  --quiet
echo "    Done."

# Create Firestore database (native mode) if not exists
echo ""
echo ">>> Setting up Firestore..."
gcloud firestore databases create \
  --location=asia-south1 \
  --quiet 2>/dev/null || echo "    Firestore already exists, skipping."

# Grant IAM roles
echo ""
echo ">>> Granting IAM roles..."
for ROLE in roles/aiplatform.user roles/datastore.user roles/logging.logWriter; do
  gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="user:$USER_EMAIL" \
    --role="$ROLE" \
    --quiet
done
echo "    Done."

# Create .env file
echo ""
echo ">>> Creating .env file..."
SERVICE_ACCOUNT=$(gcloud iam service-accounts list \
  --filter="displayName:Compute Engine default" \
  --format="value(email)" | head -1)

cat > .env << ENVEOF
MODEL="gemini-2.5-flash"
PROJECT_ID=$PROJECT_ID
REGION=$REGION
SERVICE_ACCOUNT=$SERVICE_ACCOUNT
ENVEOF
echo "    .env created."

# Set up ADC
echo ""
echo ">>> Setting up Application Default Credentials..."
gcloud auth application-default login

echo ""
echo "================================================"
echo " Setup complete!"
echo " Next: Run  bash setup/deploy.sh  to deploy."
echo "================================================"
