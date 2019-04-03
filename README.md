# QRandom
Random number generation using quantum computers.

Right now the project is in its' infancy.

# WARNING: THIS PROGRAM SHOULD NOT BE CONSIDERED CRYPTOGRAPHICALLY RANDOM UNLESS CONNECTED TO A REAL QUANTUM PROCESSOR


## This is a basic example of how to use QRandom

### You can import everything
from qrandom import *

### or just the QRandom module if you'd like to instantiate it yourself
from qrandom import Qrandom
x = QRandom()

### generate a random float between 0 and 1:
print(random())
print(x.random())

### generate a random integer in range
print(randrange(0, 5))
print(x.randrange(0, 5))

### Generate a random number n bits long, defaults to integer output
print(getrandbits(8))
print(x.getrandbits(8))

### You can also get the number in byte format
print(getrandbits(8, x="bytes"))

