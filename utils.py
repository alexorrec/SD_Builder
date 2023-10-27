import Logging
import ImageManager
import sys
import time

log = Logging.Logger()
log.log_message(msg='MAIN TESTING')

for i in range(101):
    time.sleep(0.05)
    sys.stdout.write("\r%d%%" % i)
    sys.stdout.flush()

_manager = ImageManager.ImageManager('', '/Users/alessandrocerro/Desktop/SDV5_INPUT')
_manager.testingClass()
