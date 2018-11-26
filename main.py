import time
import board
import neopixel
import adafruit_dotstar

try:
    import urandom as random  # for v1.0 API support
except ImportError:
    import random

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

led = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
led.brightness = 0.1
led[0] = (0, 255, 0)

numpix = 32  # Number of NeoPixels
pixpin = board.D1  # Pin where NeoPixels are connected

mode = 0  # Current animation effect
offset = 0  # Position of spinny eyes

rgb_colors = ([255, 0, 0],  # red
              [0, 255, 0],  # green
              [0, 0, 255])  # blue

rgb_idx = 0  # index counter - primary color we are on
color = rgb_colors[rgb_idx]
prevtime = 0

pixels = neopixel.NeoPixel(pixpin, numpix, brightness=0.4, auto_write=False)

prevtime = time.monotonic()

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if (pos < 0) or (pos > 255):
        return (0, 0, 0)
    if pos < 85:
        return (int(pos * 3), int(255 - (pos * 3)), 0)
    elif pos < 170:
        pos -= 85
        return (int(255 - pos * 3), 0, int(pos * 3))
    else:
        pos -= 170
        return (0, int(pos * 3), int(255 - pos * 3))
        
def rainbow_cycle(wait):
    for j in range(255):
        for i in range(numpix//2):
            idx = int((i * 256 / numpix//2) + j)
            pixels[i] = wheel(idx & 255)
            pixels[(numpix - 1) - i] = wheel(idx & 255)

        pixels.write()
        time.sleep(wait)
      
def color_chase(color, wait):
    for i in range(numpix//2):
        pixels[i] = color
        pixels[(numpix - 1) - i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)

# Random sparks - just one LED on at a time!
def random_sparks():
    i = random.randint(0, (numpix - 1))
    pixels[i] = color
    pixels.write()
    time.sleep(0.01)
    pixels[i] = (0, 0, 0)

# Spinny wheels (8 LEDs on at a time)
def spinny_wheels():
    global offset
    
    for i in range(0, numpix):
        c = 0

        # 4 pixels on...
        if ((offset + i) & 7) < 2:
            c = color

        pixels[i] = c  # First eye
        pixels[(numpix - 1) - i] = c  # Second eye (flipped)

    pixels.write()
    offset += 1
    time.sleep(0.05)

def color_chases():
    color_chase(RED, 0.1)  # Increase the number to slow down the color chase
    color_chase(YELLOW, 0.1)
    color_chase(GREEN, 0.1)
    color_chase(CYAN, 0.1)
    color_chase(BLUE, 0.1)
    color_chase(PURPLE, 0.1)
    
while True:
    t = 0
    
    if mode < 5:
        random_sparks()        
    elif mode < 9:
        spinny_wheels()        
    elif mode == 9:
        rainbow_cycle(0.002)
    elif mode == 10:
        color_chases()

    t = time.monotonic()

    if (t - prevtime) > 8:  # Every 8 seconds...
        mode = random.randint(1, 10)

        if mode < 9:
            if rgb_idx > 2:  # reset R-->G-->B rotation
                rgb_idx = 0

            color = rgb_colors[rgb_idx]  # next color assignment
            rgb_idx += 1

        for i in range(0, numpix):
            pixels[i] = (0, 0, 0)

        prevtime = t