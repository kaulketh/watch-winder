## A possibility to enable run at bootup is to use the _systemd_ files. _systemd_ provides a standard process for controlling what programs run when a Linux system boots up. Note that systemd is available only from the Jessie versions of Raspbian OS.

### Create A Unit File

`sudo nano /lib/systemd/system/watch_winder.service`


`sudo chmod 644 /lib/systemd/system/watch_winder.service`

### Configure systemd

`sudo systemctl daemon-reload`

`sudo systemctl enable watch_winder.service`

`sudo reboot`
