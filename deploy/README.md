# Deployment & Set-and-Forget Setup

## Cron (recommended for simple setups)

1. `chmod +x deploy/cron-setup.sh`
2. Edit the cron line
3. `crontab -e`

## Systemd (recommended for always-on NAS/Linux)

Copy the .service file, edit paths, `systemctl enable --now`.

See full instructions in main README.