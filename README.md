# tort-temp Install
Clone the repository

Create a tempwatch.sh using the sample and populate the database url with your own postgres database


Optionally install supervisor to continuously run the python script for you (including start on boot):

`sudo apt-get install python-pip`

`pip install supervisor`

`echo_supervisord_conf > /etc/supervisord.conf`

`cat >> /etc/supervisord.conf <<EOF`

`[program:tempwatch]`

`command=/home/pi/tempwatch/tempwatch.sh`

`autostart=true`

`autorestart=true`

`startretries=3`

`stderr_logfile=/var/log/tempservice.log`

`stdout_logfile=/var/log/tempservice.log`

`;user=www-data`

`;environment=SECRET_PASSPHRASE='this is secret',SECRET_TWO='another secret'`

`EOF`

Init scripts for auto start of supervisor can be found here:
https://github.com/Supervisor/initscripts

Once suitable script is placed in /etc/init.d/supervisor and is executable:

`chkconfig supervisor on`

`service supervisor start`
`
