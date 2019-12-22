import RPi.GPIO as GPIO
import time
import sys
import os
from hx711 import HX711

from blessings import Terminal
from progressive.bar import Bar
from progressive.tree import ProgressTree, Value, BarDescriptor

MAX_BAR_VALUE = 115000
BAR_WIDTH = '83%'
BAR_TYPE = 'fraction' #'fraction' or 'percentage'

def cleanAndExit():
    print "Cleaning..."
    GPIO.cleanup()
    print "Bye!"
    sys.exit()


GAIN = 64

DATA_1 = 20
CLCK_1 = 21
hx1 = HX711(DATA_1, CLCK_1, gain=GAIN)

DATA_2 = 19
CLCK_2 = 26
hx2 = HX711(DATA_2, CLCK_2, gain=GAIN)

DATA_3 = 6
CLCK_3 = 13
hx3 = HX711(DATA_3, CLCK_3, gain=GAIN)

DATA_4 = 12
CLCK_4 = 16
hx4 = HX711(DATA_4, CLCK_4, gain=GAIN)


# I've found out that, for some reason, the order of the bytes is not always th$
# Still need to figure out why does it change.
# If you're experiencing super random values, change these values to MSB or LSB$
# There is some code below to debug and log the order of the bits and the bytes.
# The first parameter is the order in which the bytes are used to build the "lo$
# The second paramter is the order of the bits inside each byte.
# According to the HX711 Datasheet, the second parameter is MSB so you shouldn'$
hx1.set_reading_format("LSB", "MSB")
hx2.set_reading_format("LSB", "MSB")
hx3.set_reading_format("LSB", "MSB")
hx4.set_reading_format("LSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have a$
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers $
# and I got numbers around 184000 when I added 2kg. So, according to the rule o$
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
#hx.set_reference_unit(113)
hx1.set_reference_unit(92)
hx2.set_reference_unit(92)
hx3.set_reference_unit(92)
hx4.set_reference_unit(92)

hx1.reset()
hx2.reset()
hx3.reset()
hx4.reset()

hx1.tare()
hx2.tare()
hx3.tare()
hx4.tare()

leaf_values = [Value(0) for i in range(4)]
bd_defaults = dict(type=Bar, kwargs=dict(max_value=MAX_BAR_VALUE, width=BAR_WID$

test_d = {
"Carb 1": BarDescriptor(value=leaf_values[0], **bd_defaults),
"Carb 2": BarDescriptor(value=leaf_values[1], **bd_defaults),
"Carb 3": BarDescriptor(value=leaf_values[2], **bd_defaults),
"Carb 4": BarDescriptor(value=leaf_values[3], **bd_defaults),
}

# Create blessings.Terminal instance
t = Terminal()
# Initialize a ProgressTree instance
n = ProgressTree(term=t)
# We'll use the make_room method to make sure the terminal
# is filled out with all the room we need
os.system('clear')
n.make_room(test_d)
#n.cursor.save()
while True:
    try:
        # These three lines are usefull to debug wether to use MSB or LSB in th$
        # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
        # Comment the two lines "val = hx.get_weight(5)" and "print val" and un$
        #np_arr8_string = hx.get_np_arr8_string()
        #binary_string = hx.get_binary_string()
        #print binary_string + " " + np_arr8_string
        
        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
        val_1 = hx1.get_weight(DATA_1)
        val_2 = hx2.get_weight(DATA_2)
        val_3 = hx3.get_weight(DATA_3)
        val_4 = hx4.get_weight(DATA_4)
        
        #print val
        n.cursor.restore()
        leaf_values[0].value = abs(val_1)
        leaf_values[1].value = abs(val_2)
        leaf_values[2].value = abs(val_3)
        leaf_values[3].value = abs(val_4)

        n.draw(test_d, BarDescriptor(bd_defaults))
        #hx.power_down()
        #hx.power_up()
        #time.sleep(0.1)
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
