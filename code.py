# Hardware: Adafruit Qt Py 2040
import adafruit_displayio_ssd1306
import displayio
from adafruit_display_text import label
import terminalio
import board
import time
from digitalio import DigitalInOut, Direction, Pull

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

time.sleep(0.025)
displayio.release_displays()    # Normally this is done first, but the terminal out breaks the display if we don't mux select first.

# Init display
WIDTH = 128
HEIGHT = 64
BORDER = 2
i2c = board.I2C()

# Init first display
display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)
# Swap to second display
pin_a.value = True
time.sleep(0.025)
# Fakeout teardown of second display
displayio.release_displays()
# Init second display
display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)
# Swap back to first display
pin_a.value = False
time.sleep(0.025)

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
text1 = "First display 0"
text_area = label.Label(terminalio.FONT, text=text1, color=0xFFFFFF, x=8, y=8)
splash.append(text_area)
text2 = "SSD1306-1"
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
text_area2.text = "SSD1306-2"
text_area.text = "Second display 0"

# Init pin for button I/O
button_pin = board.D6
button = DigitalInOut(button_pin)
button.direction = Direction.INPUT
button.pull = Pull.UP

times_pressed_display_1 = 0
times_pressed_display_2 = 0
pressed_button_1 = False
pressed_button_2 = False

# Spin for a bit to give displays time to settle before swapping back and forth. idk why this is needed but the displays bork without it.
start_time = time.monotonic()
while True:
    if time.monotonic() - start_time > 0.5:
        break

# Main loop
while True:
    # Swap to button/display 1
    pin_a.value = False
    time.sleep(0.025)
    if not button.value:
        if not pressed_button_1:
            times_pressed_display_1 += 1
            # print(f'Times pressed button 1: {times_pressed_display_1}')
            pressed_button_1 = True
            text_area.text = f'First display {times_pressed_display_1}'
            time.sleep(0.025)
    else:
        pressed_button_1 = False

    # Swap to button/display 2
    pin_a.value = True
    time.sleep(0.025)
    if not button.value:
        if not pressed_button_2:
            times_pressed_display_2 += 1
            # print(f'Times pressed button 2: {times_pressed_display_2}')
            pressed_button_2 = True
            text_area.text = f'Second display {times_pressed_display_2}'
            time.sleep(0.025)
    else:
        pressed_button_2 = False
