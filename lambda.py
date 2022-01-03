"""Module to automatically update channels in DB"""
import time
from datetime import datetime
import sys
import schedule
import controller

def refresh():
    """Calls update_channels in DB"""
    controller.update_channels()
    print(f"Channels have been updated at {datetime.now()}")

schedule.every(2).seconds.do(refresh)

while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except KeyboardInterrupt:
        sys.exit()
    except Exception:
        print("There was an error communicating with the controller, trying again in 30 minutes...")
