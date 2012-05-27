
import serial
import re
import MySQLdb
import subprocess
from rrdtool import update as rrd_update



dbName = "spudooli"
tblName = "power"
uName = "root"
pswd = "bobthefish"


hotwater = ""
wholehouse = ""
orbcolor = ""
orbsetcolor = ""


def changeorb( color ):
   global orbsetcolor
   if color == "blue":
   	if color is orbsetcolor:
   		print "color is already "+color+" so did nothing"
    	else:
   		print "Setting orb to "+color
   		orb.write('~A 8')
   elif color == "red":
   	if color is orbsetcolor:
   		print "color is already "+color+" so did nothing"
    	else:
   		print "Setting orb to "+color
   		orb.write('~A  ')
   elif color == "orange":
   	if color is orbsetcolor:
   		print "color is already "+color+" so did nothing"
    	else:
   		print "Setting orb to "+color
   		orb.write('~A "')
   elif color == "green":
   	if color is orbsetcolor:
   		print "color is already "+color+" so did nothing"
    	else:
   		print "Setting orb to "+color
   		orb.write('~A ,')
   orbsetcolor = color
   return
   
   

ser = serial.Serial(
                port='/dev/ttyUSB0',
                baudrate=57600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
)

orb = serial.Serial(
                port='/dev/ttyS4',
                baudrate=19200,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
)



db=MySQLdb.connect(user=uName, passwd=pswd,db=dbName)

c = db.cursor()
prevWatts = 0
deltaT = 0

while 1:
        line=""
        line = ser.readline()   #read a '\n' terminated line
	if line[65:69] == "hist":
		print "oops, thats the history output, ignoring"
	else:
		reading = re.search('.*<sensor>([0-9])</sensor><id>([0-9][0-9][0-9][0-9][0-9])</id><type>1</type><ch1><watts>[0]*([0-9][0-9]*).*',line)
		#print reading
		n = re.search('.*<time>([0-9][0-9]):([0-9][0-9]):([0-9][0-9]).*',line)
		#if reading is not None:
		sensor = reading.group(1)
		sensorid = reading.group(2)
		watts = reading.group(3)
		hours = n.group(1)
		mins = n.group(2)
		secs = n.group(3)

		if sensor == "0":
			wholehouse = watts
			#deltaW = int(wholehouse) - int(prevWatts)
			prevWatts = int(wholehouse)
			if int(wholehouse) < 1000:
				changeorb("green")
			elif int(wholehouse) > 2000:
				changeorb("red")
			elif int(wholehouse) > 1000:
				changeorb("orange")
			else:
				print "something didn't happen"

			#prints individual readings, so you can check it is working
			print "Whole house = "+wholehouse+"W"
			print hours+":"+mins+":"+secs
			print "Hot water = "+hotwater+"W"
			c.execute("INSERT INTO power (wholehouse, hotwater) VALUES (%s, %s)",(wholehouse, hotwater))

      #do the rrd thing
      #systemcmd = "rrdtool update current-cost-cow.rrd N:"+wholehouse+":"+hotwater
      #print systemcmd
      #subprocess.call(['rrdtool', 'update', 'current-cost-cow.rrd', 'N:', wholehouse, ':', hotwater, shell=False])
      #ret = rrd_update('current-cost-cow.rrd', 'N:%s:%s' %(wholehouse, hotwater));


			ret = rrd_update('current-cost-cow.rrd', 'N:%s:%s' %(wholehouse, hotwater));
			fo = open("/var/www/spudooli/power.txt", "w")
			fo.write(wholehouse+","+hotwater);
			fo.close()
      #ret = rrd_update('current-cost-cow.rrd', 'N:%s:%s' %(wholehouse, hotwater));


		if sensor == "1":
			hotwater = watts
