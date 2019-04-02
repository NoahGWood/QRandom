from pyquil import *
from pyquil.gates import *
import random

BPF = 53        # Number of bits in a float
RECIP_BPF = 2**-BPF

class QRandom(random.Random):

    def __init__(self):
        self.p = self._bell_state()
        self.qc = self.qvm()

    def _bell_state(self):
        return Program(H(0), CNOT(0,1))

    def __arr_to_int__(self, arr):
        return int(''.join([str(i) for i in arr]), 2)

    def __arr_to_bits__(self, arr):
        return ''.join([str(i) for i in arr])
    
    def __int_to_bytes__(self, k, x=64):
        """returns a bytes object of the integer k with x bytes"""
        #return bytes(k,x)
        return bytes(''.join(str(1 & int(k) >> i) for i in range(x)[::-1]), 'utf-8')

    def __bits_to_bytes__(self, k):
        """returns a bytes object of the bitstring k"""
        return int(k, 2).to_bytes((len(k) + 7) // 8, 'big')
    
    def qvm(self):
        return get_qc('9q-square-qvm')

    def random(self):
        """Get the next random number in the range [0.0, 1.0)."""
        x = self.getrandbits(56)
        return (int.from_bytes(self.__bits_to_bytes__(str(x)), 'big') >> 3) * RECIP_BPF

    def getrandbits(self, k):
        if k <= 0:
            raise ValueError("Number of bits should be greater than 0")
        if k != int(k):
            raise ValueError("Number of bits should be an integer")
#        print(self.qc.run_and_measure(self.p,trials=k))
        n = int(self.__arr_to_bits__(self.qc.run_and_measure(self.p,trials=k)[0]))
        return n
