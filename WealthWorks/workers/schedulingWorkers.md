# Templates

First make sure you have setup a virtual environment and installed the required dependencies for the project.
For intructions see: [README.md](..%2F..%2FREADME.md).

Note: This templates are for scheduling the newsCollector and newsCleanner workers to run every 30 minutes, you could change this to your liking.

## NewsCollector

1. File name: newsCollector.service

```text
[Unit]
Description=newsCollector

[Service]
ExecStart=/bin/bash -c '. /root/personal/WealthWorks/venv/bin/activate && /root/personal/WealthWorks/venv/bin/python3 /root/personal/WealthWorks/WealthWorks/workers/newsCollector.py'

[Install]
WantedBy=multi-user.target
```

2. File name: newsCollector.timer

```text
[Unit]
Description=Run newsCollector every 30 minutes

[Timer]
OnCalendar=*:0/30
Persistent=true

[Install]
WantedBy=timers.target
```


## NewsCleaner

1. File name: newsCleanner.service

```text
[Unit]
Description=newsCleanner

[Service]
ExecStart=/bin/bash -c '. /root/personal/WealthWorks/venv/bin/activate && /root/personal/WealthWorks/venv/bin/python3 /root/personal/WealthWorks/WealthWorks/workers/newsCleanner.py'

[Install]
WantedBy=multi-user.target
```

2. File name: newsCleanner.timer

```text
[Unit]
Description=Run newsCleanner every 30 minutes

[Timer]
OnCalendar=*:0/30
Persistent=true

[Install]
WantedBy=timers.target
```

# Activating the scheduled times

```bash
sudo mv newsCollector.service /etc/systemd/system/
sudo mv newsCollector.timer /etc/systemd/system/

sudo mv newsCleanner.service /etc/systemd/system/
sudo mv newsCleanner.timer /etc/systemd/system/

sudo systemctl daemon-reload

sudo systemctl start newsCollector.timer
sudo systemctl enable newsCollector.timer
sudo systemctl start newsCleanner.timer
sudo systemctl enable newsCleanner.timer
```

# Testing the scheduled services

## Stop timers
```bash
sudo systemctl stop myscript.timer
```

## Manually start the service
```bash
sudo systemctl start myscript.service
```

## Check the status of the service
```bash
sudo systemctl status myscript.service
```

## Start the timer if everything is working
```bash
sudo systemctl start myscript.timer
```