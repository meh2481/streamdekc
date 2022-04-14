# Hardware: Adafruit Qt Py 2040
import adafruit_displayio_ssd1306
import displayio
from adafruit_display_text import label
import terminalio
import board
import time
from digitalio import DigitalInOut, Direction

displayio.release_displays()

# Init demuxer
A = board.D10
B = board.D9
C = board.D8

pin_a = DigitalInOut(A)
pin_a.direction = Direction.OUTPUT
pin_b = DigitalInOut(B)
pin_b.direction = Direction.OUTPUT
pin_c = DigitalInOut(C)
pin_c.direction = Direction.OUTPUT

pin_a.value = False
pin_b.value = False
pin_c.value = False

# Init display

WIDTH = 128
HEIGHT = 64
BORDER = 2

i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

# Make the display context
splash = displayio.Group()
display.show(splash)

# Draw black background
color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x0
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Label text
text1 = "First display"
text_area = label.Label(terminalio.FONT, text=text1, color=0xFFFFFF, x=8, y=8)
splash.append(text_area)
text2 = "SH1107"
text_area2 = label.Label(
    terminalio.FONT, text=text2, scale=2, color=0xFFFFFF, x=9, y=44
)
splash.append(text_area2)

# Update the second display
time.sleep(0.025) # Wait for i2c calls to first display to finish
pin_a.value = True

# Fakeout a full display redraw by changing the x location of the bg image
splash.x = 1
splash.x = 0
text_area2.text = "SSD1306"
text_area.text = "Second display"

while True:
    pass
