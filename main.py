__author__ = 'marcel'

from mpd import MPDClient, MPDError
from lib.Photocell.lib.Photocell import CheckLight
from lib.FlushFMLCD.lib.LCDController import LCD
from lib.FlushFMLCD.lib.LineController import TimeLine, MPDLine, FetchLine

# MPD Client
client = MPDClient()

client.timeout = 10
client.idletimeout = None
client.connect("localhost", 6600)

# LCD
lcd = LCD(4, 20)

lcd.set_line("time", TimeLine(lcd, 1))
lcd.set_line("station", MPDLine(lcd, 2, "name", align='c', refresh_interval=10, step_interval=1))
lcd.set_line("song", MPDLine(lcd, 3, "title"))
lcd.set_line("proverb", FetchLine(lcd, 4, "http://sprichwortgenerator.de/plugin.php"))

# init
lcd.lineContainer["time"].run_every()
lcd.lineContainer["station"].run_every()
lcd.lineContainer["song"].run_every()
lcd.lineContainer["proverb"].run_every()


# define methods to run when light state changes
def light_on_method():
	client.play()
	lcd.resume()


def light_off_method():
	client.stop()
	lcd.standby()

# Check light
check_light = CheckLight(light_on_method, light_off_method)
check_light.run()