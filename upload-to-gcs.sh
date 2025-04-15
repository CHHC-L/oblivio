#!/bin/bash
set -e

if [ ! -f .env ]; then
  echo "[Error] .env file not found!"
  exit 1
fi

export $(grep -v '^#' .env | xargs)

if [ -z "$GCS_BUCKET_NAME" ]; then
  echo "Error: GCS_BUCKET_NAME is not defined in .env"
  exit 1
fi

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 /path/to/project-folder"
  exit 1
fi

LOCAL_PATH="$1"

if [ ! -d "$LOCAL_PATH" ]; then
  echo "Error: '$LOCAL_PATH' is not a valid directory."
  exit 1
fi

PROJECT_NAME=$(basename "$LOCAL_PATH")
echo "Project name detected: $PROJECT_NAME"

DESTINATION="gs://$GCS_BUCKET_NAME/$PROJECT_NAME/"

echo "Uploading contents from '$LOCAL_PATH' to '$DESTINATION'"
gsutil -m cp -r "$LOCAL_PATH"/* "$DESTINATION"
echo "Upload complete."
