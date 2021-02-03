# Create A Unit File

`sudo nano /lib/systemd/system/watch_winder.service`


`sudo chmod 644 /lib/systemd/system/watch_winder.service`

# Configure systemd

`sudo systemctl daemon-reload`

`sudo systemctl enable watch_winder.service`

`sudo reboot`
