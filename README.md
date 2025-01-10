# STT Demo Platform Services

This document provides instructions for managing the Speech-to-Text (STT) Demo Platform services on Ubuntu.

## Overview

The STT Demo Platform consists of several interconnected services that work together to provide a comprehensive speech-to-text solution. The main components are:

1. A Python-based backend running in an Anaconda environment, managed by systemd and the user `stt_service`.
2. A frontend website running in a Docker container
3. Nginx for port forwarding, configured at `/etc/nginx/sites-enabled/default`

## Backend Services

Three Python services work together to offer the long_api:

1. **Transcription Service** (`whisper_transcribe/transcribe.py`)
   - Continuously scans a folder for .mp3 files to transcribe
   - Managed by `stt-transcribe.service`

2. **Upload Service** (`whisper_transcribe/upload.py`)
   - Provides a web interface for uploading .mp3 files to the server
   - Managed by `stt-uploader.service`
   - Accessible via [https://stt4sg.fhnw.ch/long_v3/](https://stt4sg.fhnw.ch/long_v3/)

3. **Status Service** (`whisper_transcribe/status.py`)
   - Offers a web interface to check transcription status
   - Allows users to download transcriptions in various formats
   - Managed by `stt-status.service`
   - Accessible via [https://stt4sg.fhnw.ch/long_v3/status/](https://stt4sg.fhnw.ch/long_v3/status/)

4. **Short Transcription Service** (`stt/app.py`)
   - Provides a web interface for short transcriptions
   - Managed by `stt.service`
   - Accessible via [https://stt4sg.fhnw.ch/stt/](https://stt4sg.fhnw.ch/stt/)

### Deployment
They are deployed by an user `stt_service`, have an conda enviroment `stt_env` and their deployment is managed by systemd.
A helpful script for the deployment is `deploy.bash`, which automatically copies files to `/srv/` and changes the ownership to the user.
However, containers and services have to be restarted manually.

## Frontend

The main website is hosted in a Docker container:

- Configuration: `stt-demo-platform/docker-compose.yml`
- Source code: `stt-demo-platform/stt4sg-demo-app`
- URL: [https://stt4sg.fhnw.ch/](https://stt4sg.fhnw.ch/)

### Updating the Frontend

To make changes to the main website:

1. Edit the files in `stt-demo-platform/stt4sg-demo-app`
2. Rebuild the Docker container:
   ```bash
   sudo docker compose up -d --build frontend
   ```

## Managing Services
You can manage the STT services using systemd commands. For example:

- Start a service: `sudo systemctl start stt-uploader.service`
- Stop a service: `sudo systemctl stop stt-transcribe.service`
- Restart a service: `sudo systemctl restart stt-status.service`
- Check service status: `sudo systemctl status stt-uploader.service`

### Checking Latest Logs

To view the most recent logs for a service in real-time:

```bash
sudo journalctl -u <service-name> -f
```

### Editing a Service

1. Edit the service file:
   ```bash
   sudo nano /etc/systemd/system/<service-name>.service
   ```
2. After making changes, reload the systemd manager:
   ```bash
   sudo systemctl daemon-reload
   ```
3. Restart the service to apply changes:
   ```bash
   sudo systemctl restart <service-name>
   ```