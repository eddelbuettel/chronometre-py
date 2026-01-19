#!/usr/bin/env python

import time
from datetime import timedelta
import chronometre

sw1 = chronometre.Stopwatch()
time.sleep(0.05)

# Get the memory address of sw1
address = hex(id(sw1))
print(id(sw1))
print(address)

# Create sw2 from sw1's address
print(sw1.elapsed())
sw2 = chronometre.Stopwatch(address)
print(sw2.elapsed())

# Both should have similar elapsed times
#elapsed1 = sw1.elapsed()
#elapsed2 = sw2.elapsed()
#print(elapsed1)
#print(elapsed2)

#elapsed1 = sw1.elapsed_as_double()
#elapsed2 = sw2.elapsed_as_double()
#print(elapsed1)
#print(elapsed2)
