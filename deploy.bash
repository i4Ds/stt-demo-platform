#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Variables
SOURCE_DIR="$(pwd)"
DEST_DIR="/srv/stt-demo-platform/"
USER="stt_service"
GROUP="stt_service"  # Assuming the group name is the same as the user
LOG_FILE="deploy.log"

# Function to log messages
log() {
    echo "$(date +"%Y-%m-%d %H:%M:%S") : $1" | tee -a "$LOG_FILE"
}

# Start deployment
log "Starting deployment..."

# Check if the destination directory exists
if [ ! -d "$DEST_DIR" ]; then
    log "Destination directory $DEST_DIR does not exist. Creating it..."
    sudo mkdir -p "$DEST_DIR"
fi

# Copy files to the destination directory using rsync
log "Copying files from $SOURCE_DIR to $DEST_DIR..."
sudo rsync -av --delete "$SOURCE_DIR"/ "$DEST_DIR" >> "$LOG_FILE" 2>&1

# Change ownership to stt_service user and group
log "Changing ownership of $DEST_DIR to $USER:$GROUP..."
sudo chown -R "$USER":"$GROUP" "$DEST_DIR"

# (Optional) Set appropriate permissions
# For example, set directories to 755 and files to 644
log "Setting directory permissions to 755 and file permissions to 644..."
sudo find "$DEST_DIR" -type d -exec chmod 755 {} \;
sudo find "$DEST_DIR" -type f -exec chmod 644 {} \;


# Finish deployment
log "Deployment completed successfully."

exit 0