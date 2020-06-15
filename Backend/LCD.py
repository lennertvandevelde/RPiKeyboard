from RPi import GPIO
import time



class Lcd:

    def __init__(self, E=20, RS= 21, SDA=23, SCL=24, address=56):
        GPIO.setmode(GPIO.BCM)
        self.E = E
        self.RS = RS
        self.pcf = PCF8574(SDA, SCL, address)
        GPIO.setup(self.RS, GPIO.OUT)
        GPIO.setup(self.E, GPIO.OUT)
        self.send_instruction(0x38, True) #function set
        self.send_instruction(0xF) #dislplay on
        self.send_instruction(0x1) #clear dislay
      
    @property
    def E(self):
          return self._E
    @E.setter
    def E(self, value):
        self._E = value

    @property
    def RS(self):
          return self._RS
    @RS.setter
    def RS(self, value):
        self._RS = value

    def new_line(self):
        self.send_instruction(0xC0) # volgende lijn

    def send_instruction(self, value, firsti=False):
        GPIO.output(self.RS, GPIO.LOW)
        GPIO.output(self.E, GPIO.HIGH)
        self.set_data_bits(value, first=firsti)
        GPIO.output(self.E, GPIO.LOW)
        time.sleep(0.01)

    def send_character(self, value, lastc = False):
        GPIO.output(self.RS, GPIO.HIGH)
        GPIO.output(self.E, GPIO.HIGH)
        self.set_data_bits(value, first=False, last=lastc)
        GPIO.output(self.E, GPIO.LOW)
        time.sleep(0.01)

    def write_message(self, message):
        i = 0
        message = str(message)
        if len(message) < 17:
            for i in range(0, len(message)):
                if i == (len(message)-1):
                    self.send_character(ord(message[i]), lastc=True )
                else:
                    self.send_character(ord(message[i]))

        else:
            for i in range(0, 16):
                self.send_character(ord(message[i]))
            self.send_instruction(0xC0) # volgende lijn
            for i in range(16,len(message)):
                self.send_character(ord(message[i]))
                
    def clear_display(self):
        self.send_instruction(0x1) #clear dislay


    def set_data_bits(self, value, first = False, last =False):
        self.pcf.write_outputs(value, first, last)



class PCF8574:

    # Startconditie => Adres + R/W => Ack => data > Ack=> …=>Ack=>Stop 

    def __init__(self, SDA, SCL, address):
      self.SDA = SDA
      self.SCL = SCL
      GPIO.setup(self.SDA, GPIO.OUT)
      GPIO.setup(self.SCL, GPIO.OUT)
      self.address = address

    @property
    def SDA(self):
        return self._SDA
    @SDA.setter
    def SDA(self, value):
        self._SDA = value

    @property
    def SCL(self):
        return self._SCL
    @SCL.setter
    def SCL(self, value):
        self._SCL = value
      
    @property
    def address(self):
          return self._address
    @address.setter
    def address(self, value):
        self._address = value

    
    def write_outputs(self, data:int, first, last):
        print(data)
        if first:
            self._start_conditie()
            self._writebyte(self.address << 1)
            self._ack()
        self._writebyte(data)
        self._ack()
        if last:
            self._stop_conditie()
    
    def _start_conditie(self):
        print("start")
        GPIO.output(self.SDA, GPIO.HIGH)
        GPIO.output(self.SCL, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(self.SDA, GPIO.LOW)
        time.sleep(0.001)
        GPIO.output(self.SCL, GPIO.LOW)

    def _stop_conditie(self):
        GPIO.output(self.SDA, GPIO.LOW)
        GPIO.output(self.SCL, GPIO.LOW)
        time.sleep(0.001)
        GPIO.output(self.SCL, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(self.SCL, GPIO.HIGH)

    def _writebit(self,bit):
        GPIO.output(self.SDA, bit)
        time.sleep(0.001)
        GPIO.output(self.SCL, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(self.SCL, GPIO.LOW)
        time.sleep(0.001)

    def _writebyte(self,byte):
        mask = 0x80
        for i in range(0,8):
            bit = mask & byte
            bit = bit >> (7 - i)
            self._writebit(bit)
            mask = mask >> 1
        
    
    def _ack(self):
        print("ack")
        GPIO.setup(self.SDA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.output(self.SCL,1)
        value = GPIO.input(self.SDA)
        GPIO.setup(self.SDA,GPIO.OUT)
        GPIO.output(self.SCL,0)