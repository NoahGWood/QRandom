"""Random variable generator using quantum machines
"""

from math import sqrt as _sqrt
import random
import psutil
from pyquil.quil import Program
from pyquil.api import get_qc
from pyquil.gates import H, CNOT
import vm

__all__ = ["QRandom", "random", "randint", "randrange", "getstate", "setstate", "getrandbits"]

BPF = 53        # Number of bits in a float
RECIP_BPF = 2**-BPF

def bell_state():
    """Returns the Program object of a bell state operation on a quantum computer
    """
    return Program(H(0), CNOT(0, 1))

def arr_to_int(arr):
    """returns an integer from an array of binary numbers
    arr = [1 0 1 0 1 0 1] || [1,0,1,0,1,0,1]
    """
    return int(''.join([str(i) for i in arr]), 2)

def arr_to_bits(arr):
    return ''.join([str(i) for i in arr])

def int_to_bytes(k, x=64):
    """returns a bytes object of the integer k with x bytes"""
    #return bytes(k,x)
    return bytes(''.join(str(1 & int(k) >> i) for i in range(x)[::-1]), 'utf-8')

def bits_to_bytes(k):
    """returns a bytes object of the bitstring k"""
    return int(k, 2).to_bytes((len(k) + 7) // 8, 'big')

def qvm():
    """Returns the quantum computer or virtual machine"""
    return get_qc('9q-square-qvm')

def test_quantum_connection():
    """
    Tests the connection to the quantum virtual machine.
    attempts to start the virtual machine if possible
    """
    while True:
        qvm_running = False
        quilc_running = False
        for proc in psutil.process_iter():
            if 'qvm' in proc.name().lower():
                qvm_running = True
            elif 'quilc' in proc.name().lower():
                quilc_running = True
        if qvm_running is False or quilc_running is False:
            try:
                vm.start_servers()
            except Exception as e:
                raise Exception(e)
        else:
            break

class QRandom(random.Random):
    """Quantum random number generator

        Generates a random number by collapsing bell states on a
        quantum computer or quantum virtual machine.
    """

    def __init__(self):
        super().__init__(self)
        self.p = bell_state()
        self.qc = qvm()
        # Make sure we can connect to the servers
        test_quantum_connection()

    def random(self):
        """Get the next random number in the range [0.0, 1.0)."""
        return (int.from_bytes(self.getrandbits(56, 'bytes'), 'big') >> 3) * RECIP_BPF

    def getrandbits(self, k, x="int"):
        """getrandbits(k) -> x. generates an integer with k random bits"""
        if k <= 0:
            raise ValueError("Number of bits should be greater than 0")
        if k != int(k):
            raise ValueError("Number of bits should be an integer")
        out = bits_to_bytes(arr_to_bits(self.qc.run_and_measure(self.p, trials=k)[0]))
        if x in ('int', 'INT'):
            return int.from_bytes(out, 'big')
        elif x in ('bytes', 'b'):
            return out
        else:
            raise ValueError(str(x) + ' not a valid type (int, bytes)')

def _test_generator(n, func, args):
    import time
    print(n, 'times', func.__name__)
    total = 0.0
    sqsum = 0.0
    smallest = 1e10
    largest = -1e10
    t0 = time.time()
    for i in range(n):
        x = func(*args)
        total += x
        sqsum = sqsum + x*x
        smallest = min(x, smallest)
        largest = max(x, largest)
    t1 = time.time()
    print(round(t1 - t0, 3), 'sec,', end=' ')
    avg = total/n
    stddev = _sqrt(sqsum / n - avg*avg)
    print('avg %g, stddev %g, min %g, max %g\n' % \
              (avg, stddev, smallest, largest))


def _test(N=2000):
    _test_generator(N, random, ())
    _test_generator(N, getrandbits, ([512]))
# Create one instance, seeded from current time, and export its methods
# as module-level functions.  The functions share state across all uses
#(both in the user's code and in the Python libraries), but that's fine
# for most programs and is easier for the casual user than making them
# instantiate their own QRandom() instance.

_inst = QRandom()
#seed = _inst.seed
random = _inst.random
randint = _inst.randint
randrange = _inst.randrange
getstate = _inst.getstate
setstate = _inst.setstate
getrandbits = _inst.getrandbits

if __name__ == '__main__':
    _test(1)
