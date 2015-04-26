from Tkinter import *
import serial
import re
import MySQLdb
import subprocess
from rrdtool import update as rrd_update
import time
import threading
import Queue



dbName = "spudooli"
tblName = "power"
uName = "root"
pswd = "bobthefish"

global hotwater 
global wholehouse 
orbcolor = ""
orbsetcolor = ""

def changeorb( color ):
  global orbsetcolor
  orb.write('G+')
  if color == "blue":
    if color is orbsetcolor:
      statusbarvar.set("Orb is already "+color+" so did nothing")
    else:
      statusbarvar.set("Setting orb to "+color)
      orb.write('~A 8')
  elif color == "red":
    if color is orbsetcolor:
      statusbarvar.set("Orb is already "+color+" so did nothing")
    else:
      statusbarvar.set("Setting orb to "+color)
      orb.write('~A  ')
  elif color == "orange":
    if color is orbsetcolor:
      statusbarvar.set("Orb is already "+color+" so did nothing")
    else:
      statusbarvar.set("Setting orb to "+color)
      orb.write('~A "')
  elif color == "green":
    if color is orbsetcolor:
      statusbarvar.set("Orb is already "+color+" so did nothing")
    else:
      statusbarvar.set("Setting orb to "+color)
      orb.write('~A ,')
  orbsetcolor = color
  root.update_idletasks()
  return

ser = serial.Serial(
                port='/dev/ttyUSB0',
                baudrate=57600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
)

orb = serial.Serial(
                port='/dev/ttyS5',
                baudrate=19200,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
)
   
db=MySQLdb.connect(user=uName, passwd=pswd,db=dbName)

c = db.cursor()
prevWatts = 0
deltaT = 0



class GuiPart:
    def __init__(self, master, queue, endCommand):
        self.queue = queue
        # Set up the GUI
        frame = Frame(master)
        frame.pack()

        self.button = Button(
            frame, text="QUIT", fg="red", command=self.quit_pressed
            )
        self.button.pack(side=LEFT)
        self.housewattslabel = Label(root, textvariable = wholehousevar, font=("Helvetica", 22))
        self.housewattslabel.pack()

        self.orbcolourlabel = Label(root, textvariable = hotwatervar, font=("Helvetica", 22))
        self.orbcolourlabel.pack()
        # Add more GUI stuff here

        self.status = Label(master, textvariable = statusbarvar, bd=1, relief=SUNKEN, anchor=W)
        self.status.pack(side=BOTTOM, fill=X)


    def quit_pressed(self):
        root.destroy() #This will kill the application itself, not the self frame.

    def processIncoming(self):
        """
        Handle all the messages currently in the queue (if any).
        """
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                # Check contents of message and do what it says
                # As a test, we simply print it
                #hotwater = ""
                #wholehouse = ""
                orbcolor = ""
                sensor = ""
                orbsetcolor = ""
                if msg[65:69] == "hist":
                    statusbarvar.set("oops, thats the history output, ignoring")
                    root.update_idletasks()
                else:
                    reading = re.search('.*<sensor>([0-9])</sensor><id>([0-9][0-9][0-9][0-9][0-9])</id><type>1</type><ch1><watts>[0]*([0-9][0-9]*).*',msg)
                    #print reading
                    sensor = reading.group(1)
                    sensorid = reading.group(2)
                    watts = reading.group(3)

                if sensor == "0":
                    wholehouse = watts
                    #deltaW = int(wholehouse) - int(prevWatts)
                    prevWatts = int(wholehouse)
                    if int(wholehouse) < 2499:
                        changeorb("green")
                    elif int(wholehouse) > 3500:
                        changeorb("red")
                    elif int(wholehouse) > 2500:
                        changeorb("orange")
                    else:
                        print "something didn't happen"

                    #prints individual readings, so you can check it is working
                    #print "Whole house = "+wholehouse+"W"
                    wholehousevar.set(wholehouse)
                                        
                    c.execute("INSERT INTO power (wholehouse, hotwater) VALUES (%s, %s)",(wholehouse, hotwater))

                    ret = rrd_update('/var/www/scripts/current-cost-cow/current-cost-cow.rrd', 'N:%s:%s' %(wholehouse, hotwater));
                    fo = open("/var/www/spudooli/power.txt", "w")
                    fo.write(wholehouse+","+hotwater);
                    fo.close()

                if sensor == "1":
                    hotwater = watts
                    hotwatervar.set(hotwater)
                    root.update_idletasks()
            except Queue.Empty:
                pass

class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI. We spawn a new thread for the worker.
        """
        self.master = master

        # Create the queue
        self.queue = Queue.Queue()

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.endApplication)

        # Set up the thread to do asynchronous I/O
        # More can be made if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    def periodicCall(self):
        """
        Check every 100 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(100, self.periodicCall)

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select()'.
        One important thing to remember is that the thread has to yield
        control.
        """
        while self.running:
            # To simulate asynchronous I/O, we create a random number at
            # random intervals. Replace the following 2 lines with the real
            # thing.
            msg=""
            msg = ser.readline()
            self.queue.put(msg)

    def endApplication(self):
        self.running = 0


root = Tk()
root.title("Current Cost Cow")
root.geometry("300x200+5+5")
wholehousevar = StringVar()
wholehousevar.set('----')
hotwatervar = StringVar()
hotwatervar.set('----')
statusbarvar = StringVar()
statusbarvar.set(' ')
client = ThreadedClient(root)
root.mainloop()
root.master.destroy() # optional; see description below