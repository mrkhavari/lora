from SX127x.LoRa import *
from SX127x.board_config import BOARD
import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
BOARD.setup()

class RECEIVER(LoRa):
    def __init__(self,verbose=False):
        super(RECEIVER,self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0,0,0,0,0,0])
    
    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
            sleep(1)
    
    def on_rx_done(self):
        print(str(datetime.now()).split('.')[0] + "[Received]")
        self.clear_irq_flags(RxDone=1)
        payload=self.read_payload(nocheck=True)
        print(bytes(payload).decode("utf-8" ,"ignore"))
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        
receiver=RECEIVER(verbose=False)
receiver.set_mode(MODE.STDBY)

try:
    receiver.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("")
    sys.stderr.write("Keyboardinterrup")
    GPIO.cleanup()
finally:
    sys.stdout.flush()
    print("")
    GPIO.cleanup()
    receiver.set_mode(MODE.SLEEP)
    BOARD.teardown()



    
    
    
    
    
    