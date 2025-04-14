#!/bin/bash

if [ ! -f .env ]; then
  echo "[Error] .env file not found!"
  exit 1
fi

export $(grep -v '^#' .env | xargs)

if [ -z "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
  echo "[Error] GOOGLE_APPLICATION_CREDENTIALS is not defined in .env"
  exit 1
fi

JSON_PATH="$GOOGLE_APPLICATION_CREDENTIALS"
if [ ! -f "$JSON_PATH" ]; then
  echo "[Error] JSON credentials file not found at: $JSON_PATH"
  exit 1
fi

# Escape double quotes and newlines for Heroku
ESCAPED_JSON=$(python3 -c "import json; print(json.dumps(json.load(open('$JSON_PATH'))))")

echo "Setting GOOGLE_APPLICATION_CREDENTIALS_JSON in Heroku..."
heroku config:set GOOGLE_APPLICATION_CREDENTIALS_JSON="$ESCAPED_JSON"
echo "Done!"
