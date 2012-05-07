#http://www.daniweb.com/software-development/python/threads/265625/stuck-gui-with-pygtk-and-threads
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

hotwater = ""
wholehouse = ""
orbcolor = ""
orbsetcolor = ""


class MainWindow(gtk.Window):
   
   #displayText = 
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
       #print "Got to heere"
       #self.addTextToWidget("DEBUG:")
       #self.getSerial(button)
   
   def getSerial(self):
       self.changeorb("red")
       self.addTextToWidget("DEBUG:")
       #while 1: 
         #readings = self.serial.readline()#.strip().split(' ') # the readings are separated by space
         
         #if (readings.find('%M')!=-1):
            # readings = readings.strip().split(' ')
            # if (len(readings) == 10):
               # self.addTextToWidget(getTime() + ": " + "CO2:" + readings[1] + " Temp:" +readings[2] + " Light:" +readings[3] + " FAN:" +readings[4] + " CO2ON:" + readings[5] + " CO2LOSS:" + readings[6] + " CO2INJ:" + readings[7] + " HighBias:" + str(int(readings[8]) -200) + " LowBias:" + readings[9])
        # else: 
            # self.addTextToWidget("DEBUG: " + readings.strip())
   def addTextToWidget(self, newText):
          print "but to here?"
          self.textview.get_buffer().insert(self.textview.get_buffer().get_start_iter(), newText) 
    
   def changeorb(self,  color):
       global orbsetcolor
       if color == "blue":
        if color is orbsetcolor:
          print "color is already "+color+" so did nothing"
        else:
          print "Setting orb to "+color
          self.orb.write('~A 8')
       elif color == "red":
        if color is orbsetcolor:
          print "color is already "+color+" so did nothing"
        else:
          self.addTextToWidget("Setting orb to "+color)
          self.orb.write('~A  ')
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


if __name__ == '__main__':
    gobject.threads_init()
    gtk.gdk.threads_init()
    w = MainWindow()
    w.connect("destroy", lambda _: gtk.main_quit())
    gtk.main()