# VueFlaskAuth
Template for VueFlask Dashboards. Using the [CoreUI](https://coreui.io/vue/) theme.  
This template is not finished yet but a (working) example of combinding Vue, Flask and JWT for authentication.

# Configs
Nginx
```
location / {
  include uwsgi_params;
  uwsgi_pass unix:/tmp/tussentool.sock;
  uwsgi_read_timeout 300;
}
```

Supervisord
```
[program:vuedash]
directory=/path/to/VueFlaskAuth
command=uwsgi --ini vuedash.ini
environment=PATH="/path/to/VueFlaskAuth/venv/bin"
stopsignal=QUIT
autostart=true
autorestart=true
stopasgroup=true
stderr_logfile=/path/to/VueFlaskAuth/logs/error.log
stderr_logfile_maxbytes=100KB
stderr_logfile_backups=3
stdout_logfile=/path/to/VueFlaskAuth/logs/output.log
stdout_logfile_maxbytes=100KB
stdout_logfile_backups=3
priority=998
```

# Installation / preparation

On a clean machine
```bash
sudo apt update
sudo apt upgrade
sudo apt install -y vim git python3-dev python3-pip virtualenv npm nodejs libmariadbclient-dev uwsgi supervisor python3-flask uwsgi-plugin-python
```

Import the following SQL
```sql
CREATE DATABASE vuedash;

GRANT ALL PRIVILEGES ON vuedash.* TO 'dbuser'@'localhost' IDENTIFIED BY 'password1234';

USE vuedash;

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(128) DEFAULT NULL,
  `pass` varchar(128) DEFAULT NULL,
  `email` varchar(128) DEFAULT NULL,
  `firstname` varchar(128) DEFAULT NULL,
  `lastname` varchar(128) DEFAULT NULL,
  `lastseen` timestamp NULL DEFAULT NULL,
  `lastip` varchar(50) DEFAULT NULL,
  `created` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `users` (`user`, `pass`, `email`, `firstname`, `lastname`, `created`) VALUES 
('admin', '$2b$10$DA8P2QoKoTVrLoi2NYJLXuXeFJ8mmyh/HCAtdm6t8FAuwhS/IVjOi', 'example@example.org', 'Admin', 'User', '2018-11-11 10:36:45');

```
It creates a users with username `admin` and password `testtest`

Edit the config.yaml

# Run in dev-mode

Run both the python backend
```shell
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
FLASK_APP=run.py FLASK_DEBUG=1 flask run
```
To exit the venv `deactivate`

and the Vue frontend
```shell
cd frontend
npm run dev
```

In 2 seperate terminal windows

# Building
Make sure the address `baseUrl` in `frontend/src/store/index.js` is correct
```shell
npm run build
uwsgi --init vuedash.ini

or

sudo supervisorctl start vuedash
```

# TODO
* Forgot password
* User Management
  * Add user
* Add favicon and enable them in `run.py`