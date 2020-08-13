import sys
from time import sleep
sys.path.insert(0, '../../pySX127x')        
from SX127x.LoRa import *
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD
import RPi.GPIO as GPIO


BOARD.setup()
GPIO.setwarnings(False)

class TRANS(LoRa):
    tx_counter = 0
    def __init__(self, verbose=False):
        super(TRANS, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([1,0,0,0,0,0])

    def start(self):
        self.tx_counter = 0
        BOARD.led_on()
        self.write_payload([0x0f])
        self.set_mode(MODE.TX)
        while True:
            sleep(1)
            
    def on_tx_done(self):
        self.set_mode(MODE.STDBY)
        self.clear_irq_flags(TxDone=1)
        sys.stdout.flush()
        self.tx_counter += 1
        sys.stdout.write("\rtx #%d" % self.tx_counter)
        sleep(0.01)
        rawinput = "che khabar?\r\n"
        data = [int(hex(ord(c)), 0) for c in rawinput]
        self.write_payload(data)
        BOARD.led_on()
        self.set_mode(MODE.TX)



lora = TRANS(verbose=False)
lora.set_pa_config(pa_select=1)

try:
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("")
    sys.stderr.write("KeyboardInterrupt\n")
finally:
    sys.stdout.flush()
    print("")
    lora.set_mode(MODE.SLEEP)
    print(lora)
    BOARD.teardown()
