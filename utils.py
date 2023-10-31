import Logging
import ImageManager
import sys
import time


# TODO: implementare percorso di salvataggio con relativi dati
# TODO: rivedere la gestione delle eccezioni

log = Logging.Logger()
log.log_message(msg='MAIN TESTING')

_manager = ImageManager.ImageManager('', '/Users/alessandrocerro/Desktop/SDV5_INPUT')
_manager.send_toPipe()

