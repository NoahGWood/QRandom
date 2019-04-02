from pyquil import *
from pyquil.gates import *
from math import log as _log, exp as _exp, pi as _pi, e as _e, ceil as _ceil
from math import sqrt as _sqrt, acos as _acos, cos as _cos, sin as _sin
import random
import vm
import psutil

BPF = 53        # Number of bits in a float
RECIP_BPF = 2**-BPF

class QRandom(random.Random):

    def __init__(self):
        self.p = self._bell_state()
        self.qc = self.qvm()
        self.gauss_next = None

        # Make sure we can connect to the servers
        while True:
            try:
                if self.__test_quantum_connection__() == False:
                    vm.start_servers()
                else:
                    break
            except Exception as e:
                raise Exception(e)
    def __test_quantum_connection__(self):
        while True:
            qvm = False
            quilc = False
            for proc in psutil.process_iter():
                if 'qvm' in proc.name().lower():
                    qvm = True
                elif 'quilc' in proc.name().lower():
                    quilc = True
            if qvm == False or quilc == False:
                vm.start_servers()
            else:
                break
    
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
    print(round(t1-t0, 3), 'sec,', end=' ')
    avg = total/n
    stddev = _sqrt(sqsum/n - avg*avg)
    print('avg %g, stddev %g, min %g, max %g\n' % \
              (avg, stddev, smallest, largest))


def _test(N=2000):
    _test_generator(N, random, ())
    _test_generator(N, normalvariate, (0.0, 1.0))
    _test_generator(N, lognormvariate, (0.0, 1.0))
    _test_generator(N, vonmisesvariate, (0.0, 1.0))
    _test_generator(N, gammavariate, (0.01, 1.0))
    _test_generator(N, gammavariate, (0.1, 1.0))
    _test_generator(N, gammavariate, (0.1, 2.0))
    _test_generator(N, gammavariate, (0.5, 1.0))
    _test_generator(N, gammavariate, (0.9, 1.0))
    _test_generator(N, gammavariate, (1.0, 1.0))
    _test_generator(N, gammavariate, (2.0, 1.0))
    _test_generator(N, gammavariate, (20.0, 1.0))
    _test_generator(N, gammavariate, (200.0, 1.0))
    _test_generator(N, gauss, (0.0, 1.0))
    _test_generator(N, betavariate, (3.0, 3.0))
    _test_generator(N, triangular, (0.0, 1.0, 1.0/3.0))

# Create one instance, seeded from current time, and export its methods
# as module-level functions.  The functions share state across all uses
#(both in the user's code and in the Python libraries), but that's fine
# for most programs and is easier for the casual user than making them
# instantiate their own Random() instance.

_inst = QRandom()
seed = _inst.seed
random = _inst.random
uniform = _inst.uniform
triangular = _inst.triangular
randint = _inst.randint
choice = _inst.choice
randrange = _inst.randrange
sample = _inst.sample
shuffle = _inst.shuffle
choices = _inst.choices
normalvariate = _inst.normalvariate
lognormvariate = _inst.lognormvariate
expovariate = _inst.expovariate
vonmisesvariate = _inst.vonmisesvariate
gammavariate = _inst.gammavariate
gauss = _inst.gauss
betavariate = _inst.betavariate
paretovariate = _inst.paretovariate
weibullvariate = _inst.weibullvariate
getstate = _inst.getstate
setstate = _inst.setstate
getrandbits = _inst.getrandbits

if __name__ == '__main__':
    _test(2000)

