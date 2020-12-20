#inspired of ajgbarnes

from time import sleep
from datetime import datetime
import os
import signal
from star import Star


# Get environment variables
DELAY = float(os.environ["DELAY"]) if "DELAY" in os.environ else 1
STARTTIME = os.environ["STARTTIME"] if "STARTTIME" in os.environ else "0000"
STOPTIME = os.environ["STOPTIME"] if "STOPTIME" in os.environ else "2359"
ON_BRIGHTNESS = float(os.environ["ON_BRIGHTNESS"]) if "ON_BRIGHTNESS" in os.environ else 0.8
OFF_BRIGHTNESS = float(os.environ["OFF_BRIGHTNESS"]) if "OFF_BRIGHTNESS" in os.environ else 0.3



class GracefulKiller:
  kill_now = False
  signals = {
    signal.SIGINT: 'SIGINT',
    signal.SIGTERM: 'SIGTERM'
  }

  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self, signum, frame):
    print("\nReceived {} signal".format(self.signals[signum]))
    print("Cleaning up resources. End of the program")
    self.kill_now = True
    quit()



if __name__ == '__main__':
    star = Star(pwm=True)
    leds = star.leds
    start=0
    length=5
    killer = GracefulKiller()
    while not killer.kill_now:
        now = datetime.now().strftime("%H%M")
        if now >= STARTTIME and now < STOPTIME:
            star.inner.value=OFF_BRIGHTNESS
            leds[1].value=ON_BRIGHTNESS
            for x in range(25):
                if(x % length == start):
                    leds[x+1].value=ON_BRIGHTNESS
                else:
                    leds[x+1].value=OFF_BRIGHTNESS
            start=(start+1)%length
            sleep(DELAY)
        else:
            if star.is_active:
                star.close()
                star = Star(pwm=True)
                leds = star.leds
                star.off()
            sleep(60)
            
