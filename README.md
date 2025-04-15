# Oblivio

A lightweight, private code upload platform designed for code storage & display with access control.

From the owner's side, it provides a simple script to upload files to a Google Cloud Storage bucket.

From the visitors' side, it verifies visitors' identity via email, and allows specific visitors to view the uploaded files. Only visitors with whitelisted email domains (configured by owner) are allowed to access the system.

---

## Features

- **Email Whitelist Verification**  
  Login and registration are restricted to users from approved domains via email verification codes.

- **One-time Code Upload**  
  Uploaded files are stored securely and persistently in GCS. No version control or re-upload needed.

- **Web-Based & Lightweight**  
  Built with Flask, deployable to Heroku (hopefully portable to any other platform).

- **Modular Design**  
  Clean separation between authentication, upload logic, routing, and configuration.

---

## Core Modules

### 1. Auth (Email Verification)

- Check email domain against a predefined whitelist.
- Send verification code via email.
- Establish session/token after successful verification.

### 2. Showcase

- Display uploaded files to verified users.
- Provide a simple interface to view files.

### 3. File Upload

- Transfers files to a configured GCS bucket.

### 4. Configuration & Logging

- Uses `.env` for environment settings.

---

## Testing (to be done)

Unit tests under the `tests/` directory.

```bash
pytest tests/
```

---

## Deployment

Deployment is streamlined for Heroku.  
Use the provided `.env.template` to configure environment variables.

Basically:
1. Create a new Heroku app and config it.
2. Set up Google Cloud Storage and service account.
    - Create a GCS bucket, deal with permissions, generate credentials and fill in your local `.env` file.
    - Upload files on GCS web interface, or use `upload-to-gcs.sh` script.
3. Create an email account for sending verification codes. 
    - If use gmail, set up "less secure app access" and generate an app password.
    - Then fill in your local `.env` file with email credentials.
4. Get the `.env` ready and run `set-heroku.sh`, which will set the environment variables in Heroku.
5. Push the code to Heroku and run the app.
