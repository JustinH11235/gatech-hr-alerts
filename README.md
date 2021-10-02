# gatech-hr-alerts

# How to Use

1. sudo cp -i alert_script.py /bin
2. sudo chmod +x /bin/alert_script.py
2. sudo crontab -e
3. @reboot .venv/bin/python3 /bin/alert_script.py &
