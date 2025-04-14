#!/bin/bash

if [ ! -f .env ]; then
  echo "[Error] .env file not found!"
  exit 1
fi

export $(grep -v '^#' .env | xargs)

##################################################
# Google Application Credentials
##################################################

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

##################################################
# Whitelist Domains
##################################################

if [ -z "$WHITELIST_DOMAINS" ]; then
  echo "[Error] WHITELIST_DOMAINS is not defined in .env"
  exit 1
fi

echo "Setting WHITELIST_DOMAINS in Heroku..."
heroku config:set WHITELIST_DOMAINS="$WHITELIST_DOMAINS"
echo "Done!"

##################################################
# Mail Configuration
##################################################

if [ -z "$MAIL_USERNAME" ]; then
  echo "[Error] MAIL_USERNAME is not defined in .env"
  exit 1
fi

if [ -z "$MAIL_PASSWORD" ]; then
  echo "[Error] MAIL_PASSWORD is not defined in .env"
  exit 1
fi

if [ -z "$MAIL_SERVER" ]; then
  echo "[Error] MAIL_SERVER is not defined in .env"
  exit 1
fi

if [ -z "$MAIL_PORT" ]; then
  echo "[Error] MAIL_PORT is not defined in .env"
  exit 1
fi

if [ -z "$MAIL_USE_TLS" ]; then
  echo "[Error] MAIL_USE_TLS is not defined in .env"
  exit 1
fi

echo "Setting Mail configuration in Heroku..."
heroku config:set MAIL_USERNAME="$MAIL_USERNAME"
heroku config:set MAIL_PASSWORD="$MAIL_PASSWORD"
heroku config:set MAIL_SERVER="$MAIL_SERVER"
heroku config:set MAIL_PORT="$MAIL_PORT"
heroku config:set MAIL_USE_TLS="$MAIL_USE_TLS"
echo "Done!"