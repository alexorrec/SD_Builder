import Logging
import ImageManager
import sys
import time

log = Logging.Logger()
log.log_message(msg='MAIN TESTING')

_manager = ImageManager.ImageManager('', 'C:/Users/cerroale/Desktop/TESTPY')
_manager.testingClass()