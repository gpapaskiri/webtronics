# Webtropics

app for users posts

## Global Requirements

1. Debian-like system
2. Python 3.8
3. Pip
4. Postgres

## Pre-Installation

1. Configure postgres (create new user and database, for
   example https://losst.pro/ustanovka-postgresql-ubuntu-16-04?ysclid=lctjuo3nn2800527354)

## Installation

1. Open terminal and change directory to **/opt**.
2. Run "git clone https://github.com/gpapaskiri/webtronics.git". In opt will appear folder **webtronics**.
3. Change owner for folder to user with sudoers (for example, **sudo chown username. -R webtronics**).
4. Move to directory webtronics and run **pip install -r requirements.txt**.
5. In **config.yaml** change settings for connecting to database in section **postgres**.
6. Run **python main.py createdb**. It will create all tables and relations.
7. In **config.yaml** change server settings int section **uvicorn**
8. In **.env** file change _**secret**_ value. It will user for bearer authentication.
9. Run **python main.py**

## Usage

For documentation open **http://server_ip:port/docs** (alternative documentation **http://server_ip:port/redoc**).

## Run as service

Create in **/etc/systemd/system/** file **webtronics** with next content:

[Unit]\
Description=Webtropics app\
After=syslog.target\
After=network.target

[Service]
Type=simple\
User=root\
WorkingDirectory=/opt/webtronics\
ExecStart=/usr/bin/python3.8 /opt/webtronics/main.py\
RestartSec=5\
Restart=always

[Install]\
WantedBy=multi-user.target


