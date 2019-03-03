Automatically starting Cowrie with systemd
###########################################

NOTE: untested

* Copy the file `systemd/system/cowrie.socket` to `/etc/systemd/system`

* Copy the file `systemd/system/cowrie.service` to `/etc/systemd/system`

* Modify etc/cowrie.cfg to connect to systemd:

    [ssh]
    listen_endpoints = systemd:domain=INET6:index=0

    [telnet]
    listen_endpoints = systemd:domain=INET6:index=1

* Modify `bin/cowrie` script like this:

  * Change DAEMONIZE="" line to DAEMONIZE="-n"
  * Change #STDOUT="no" line to STDOUT="yes"

* Run sudo systemctl start cowrie.socket && sudo systemctl enable cowrie.socket
