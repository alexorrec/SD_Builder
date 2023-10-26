import Logging
import ImageManager

log = Logging.Logger()
log.log_message(msg='QUESTO è UN TEST', a='ciao', b='ciao')

_manager = ImageManager.ImageManager('', 'C:\\Users\\cerroale\\Desktop\\TESTPY\\')
_manager.testingClass()
