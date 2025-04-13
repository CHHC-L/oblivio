# Oblivio

A lightweight, private code upload platform designed for code storage & display with access control. It provides a streamlined mechanism to upload code files, verify visitors' identity via email, and store them in cloud storage (Google Cloud Storage).

Only visitors with whitelisted email domains (configured by user) are allowed to access the system.

---

## Features (Developping)

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
- Send 6-digit verification code via email.
- Establish session/token after successful verification.

### 2. File Upload

- Accepts single-file uploads (future-ready for batch support).
- Validates file size and type before upload.
- Transfers files to a configured GCS bucket.
- Generates and returns a storage URL or internal reference.

### 3. Configuration & Logging

- Uses `.env` for environment settings.

---

## Testing

Unit tests under the `tests/` directory.

```bash
pytest tests/
```

---

## Deployment

Deployment is streamlined for Heroku.  
Use the provided `.env.template` to configure environment variables.

Detailed deployment instructions are available internally.

