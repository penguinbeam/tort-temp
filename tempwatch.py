#!/usr/bin/python
#install python-psycopg2

import time, sys
import signal

import os
import psycopg2
import urlparse
import psycopg2.extras

class GracefulInterruptHandler(object):

    def __init__(self, sig=signal.SIGINT):
        self.sig = sig

    def __enter__(self):

        self.interrupted = False
        self.released = False

        self.original_handler = signal.getsignal(self.sig)

        def handler(signum, frame):
            self.release()
            self.interrupted = True

        signal.signal(self.sig, handler)

        return self

    def __exit__(self, type, value, tb):
        self.release()

    def release(self):

        if self.released:
            return False

        signal.signal(self.sig, self.original_handler)

        self.released = True

        return True

#  filename = "/home/pi/tempwatch/temp1data.log"

#ls -l /sys/bus/w1/devices/ | grep -e "[0-9][0-9]:[0-9][0-9] [0-9][0-9]-" | awk '{print $9}'


dataFile = [ "/sys/bus/w1/devices/28-021573383cff/w1_slave","/sys/bus/w1/devices/28-021573a916ff/w1_slave","/sys/bus/w1/devices/28-021573a938ff/w1_slave","/sys/bus/w1/devices/28-03157478d0ff/w1_slave" ]


#dataFile = [ "/sys/bus/w1/devices/28-000006532e6e/w1_slave" ]

with GracefulInterruptHandler() as h:
	while True:
                timestamp = time.strftime("%H:%M %d/%m") 
                tempForDB = [];

                for x in xrange(0, len(dataFile)):
                #for x in xrange(0, 4):
#                        print(dataFile[x]);

                        tfile = open(dataFile[x])
                       	text = tfile.read()
		        tfile.close()

		        temperature_data = text.split()[-1]
		        temperature = float(temperature_data[2:])
		        temperature = temperature / 1000

                        tempForDB.append(round(temperature, 2));

#		datafile = open(filename, "a", 1)
#		datafile.write(str(temperature) + timestamp + "\n")
#		datafile.close()

                urlparse.uses_netloc.append("postgres")
                url = urlparse.urlparse(os.environ["DATABASE_URL"])
                
                try:
                    conn = psycopg2.connect(
                        database=url.path[1:],
                        user=url.username,
                        password=url.password,
                        host=url.hostname,
                        port=url.port
                    )
                except:
                    print "I am unable to connect to the database"

                cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                SQL = "INSERT INTO tempdata (time,tort1,tort2,tort3,tort4) VALUES (%s, %s, %s, %s, %s);"
                data = (timestamp, tempForDB[0], tempForDB[1], tempForDB[2], tempForDB[3],)
                try:
                    cur.execute(SQL, data) 
                except:
                    print "I can't INSERT"
                conn.commit()
                cur.close()
                conn.close()


		time.sleep(300)
		if h.interrupted:
			print "\nClosing gracefully"
#			datafile.close()
	     		break
