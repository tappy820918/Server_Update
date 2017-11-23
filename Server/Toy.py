__version__ = '0.0.2'
import time
from datetime import datetime


if __name__ == '__main__':
    Time = datetime.now()
    while(1):
        print "[ Toy version",__version__,']\t @', Time
        time.sleep(1)
