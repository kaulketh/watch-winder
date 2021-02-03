# Create A Unit File

`sudo nano /lib/systemd/system/watch_winder.service`

* `[Unit]
  Description=My Sample Service After=multi-user.target

[Service]
Type=idle ExecStart=/usr/bin/python /home/pi/sample.py

[Install]
WantedBy=multi-user.target`

`sudo chmod 644 /lib/systemd/system/watch_winder.service`

# Configure systemd

`sudo systemctl daemon-reload`
`sudo systemctl enable watch_winder.service`
`sudo reboot`