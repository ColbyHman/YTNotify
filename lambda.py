import schedule
import controller
from datetime import datetime
import time

def refresh():
    controller.update_channels()
    print("Channels have been updated at {0}".format(datetime.now()))

schedule.every(30).minutes.do(refresh)

while(True):
    try:
        schedule.run_pending()
        time.sleep(1)
    except KeyboardInterrupt:
        exit(0)
    except:
        print("There was an error communicating with the controller, trying again in 30 minutes...")