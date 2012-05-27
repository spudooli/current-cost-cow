import threading, thread
import gobject, gtk
import serial
import MySQLdb
import re
import gobject
 
dbName = "spudooli"
tblName = "power"
uName = "root"
pswd = "bobthefish"

orbsetcolor = "blue"

class MainWindow(gtk.Window):
   
   def __init__(self):
       self.displayText = "program start: "
       self.ser = serial.Serial(port='/dev/ttyUSB0', baudrate=57600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS )
       self.orb = serial.Serial(port='/dev/ttyS4', baudrate=19200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS )
       self.viable = True
       #Window
       super(MainWindow, self).__init__()
       #VBOX
       vb = gtk.VBox()
       self.add(vb)       
       #Scrolling Window
       self.set_size_request(300, 400)
       sw = gtk.ScrolledWindow()
       sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
       sw.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
       sw.set_border_width(10)
       self.textview = gtk.TextView()
       textbuffer = self.textview.get_buffer()
       textbuffer.set_text(self.displayText)
       sw.add(self.textview)
       vb.pack_start(sw)
       #Button for Scrolling Window
       swButton = gtk.Button(stock=gtk.STOCK_OK)
       vb.pack_start(swButton)
       swButton.connect('clicked', self.on_swButton_clicked)
       #show All
       self.show_all()
   
   def on_swButton_clicked(self, button):
       threading.Thread(target=self.getSerial).start()
   
   def getSerial(self):
       hotwater = ""
       wholehouse = ""
       orbcolor = ""
       orbsetcolor = ""
       prevWatts = 0
       db=MySQLdb.connect(user=uName, passwd=pswd,db=dbName)
       self.c = db.cursor()
       self.ser = serial.Serial(port='/dev/ttyUSB0', baudrate=57600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS )
       self.orb = serial.Serial(port='/dev/ttyS4', baudrate=19200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS )
       while 1:
         line=""
         line = self.ser.readline()   #read a '\n' terminated line
         if line[65:69] == "hist":
            print "oops, thats the history output, ignoring"
         else:
            #print "running the thing"
            reading = re.search('.*<sensor>([0-9])</sensor><id>([0-9][0-9][0-9][0-9][0-9])</id><type>1</type><ch1><watts>[0]*([0-9][0-9]*).*',line)
            print reading
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
                self.changeorb("green")
              elif int(wholehouse) > 2000:
                self.changeorb("red")
              elif int(wholehouse) > 1000:
                self.changeorb("orange")
              else:  
                print "something didn't happen"

              #prints individual readings, so you can check it is working
              self.addTextToWidget("Whole house = "+wholehouse+"W ")
              self.addTextToWidget( hours+":"+mins+":"+secs)
              self.addTextToWidget( " Hot water = "+hotwater+"W\n")

              self.c.execute("INSERT INTO power (wholehouse, hotwater) VALUES (%s, %s)",(wholehouse, hotwater))
              
              # Open a file
              fo = open("/var/www/spudooli/power.txt", "w")
              fo.write(wholehouse+","+hotwater);
              fo.close()

            if sensor == "1":
              hotwater = watts
   
   def addTextToWidget(self, newText):
       self.textview.get_buffer().insert(self.textview.get_buffer().get_start_iter(), newText) 
    
   def changeorb(self,  color):
       global orbsetcolor
       if color == "blue":
        if color is orbsetcolor:
          self.addTextToWidget("color is already "+color+" so did nothing"+"\n")
        else:
          self.addTextToWidget("Setting orb to "+color+"\n")
          self.orb.write('~A 8')
       elif color == "red":
        if color is orbsetcolor:
          self.addTextToWidget("color is already "+color+" so did nothing"+"\n")
        else:
          self.addTextToWidget("Setting orb to "+color+"\n")
          self.orb.write('~A  ')
       elif color == "orange":
        if color is orbsetcolor:
          self.addTextToWidget("color is already "+color+" so did nothing"+"\n")
        else:
          self.addTextToWidget("Setting orb to "+color+"\n")
          self.orb.write('~A "')
       elif color == "green":
        if color is orbsetcolor:
          self.addTextToWidget("color is already "+color+" so did nothing"+"\n")
        else:
          self.addTextToWidget("Setting orb to "+color+"\n")
          self.orb.write('~A ,')
       orbsetcolor = color
       return


if __name__ == '__main__':
    gobject.threads_init()
    gtk.gdk.threads_init()
    w = MainWindow()
    w.connect("destroy", lambda _: gtk.main_quit())
    w.set_title("Current Cost Cow")
    gtk.main()