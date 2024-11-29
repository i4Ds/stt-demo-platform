# Restart relevant services to apply changes
sudo systemctl restart stt-transcribe.service
sudo systemctl restart stt-uploader.service
sudo systemctl restart stt-status.service
sudo systemctl restart stt.service



# Reload systemd to recognize any changes in service files
# UNCOMMENT TO RESTART DAEMON.
# sudo systemctl daemon-reloa