import RPi.GPIO as GPIO
from time import sleep
import spidev
import numpy as np

ST7567_DISPLAY_ON =                 0b10101111 # AF
ST7567_DISPLAY_OFF =                0b10101110 # AE
ST7567_SET_START_LINE =             0b01000000 # 40
ST7567_SET_PAGE_ADDRESS =           0b10110000 # B0
ST7567_SET_COLUMN_ADDRESS_MSB =     0b00010000 # 10
ST7567_SET_COLUMN_ADDRESS_LSB =     0b00001111 # 0F
ST7567_SEG_DIRECTION_NORMAL =       0b10100000 # A0
ST7567_SEG_DIRECTION_REVERSE =      0b10100001 # A1
ST7567_INVERSE_DISPLAY_ON =         0b10100111 # A7
ST7567_INVERSE_DISPLAY_OFF =        0b10100110 # A6
ST7567_ALL_PIXEL_ON =               0b10100101 # A5
ST7567_ALL_PIXEL_OFF =              0b10100100 # A4
ST7567_BIAS_SELECT_1OVER9 =         0b10100010 # A3
ST7567_BIAS_SELECT_1OVER7 =         0b10100011 # A2
ST7567_RESET =                      0b11100010 # E2
ST7567_COM_DIRECTION_REVERSE =      0b11001000 # C8
ST7567_COM_DIRECTION_NORMAL =       0b11000000 # C0
ST7567_POWER_CONTROL =              0b00101000 # 29
ST7567_REGULATION_RATIO =           0b00100000 # 20
ST7567_SET_CONTRAST =               0b10000001 # 81
ST7567_SET_BOOSTER =                0b11111000 # F8

test_image = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xC1,0xC0,0xFE,0xC0,0xC1,0xDF,0xCF,0xC1,0xF8,0xC1,0xCF,0xDF,0xC3,0xF8,0xC1,0xF8,
              0xC3,0xDF,0xDE,0xCC,0xE1,0xE1,0xCC,0xDF,0xCF,0xC6,0xF0,0xF0,0xC6,0xCF,0xCC,0xC8,
              0xD2,0xC4,0xCC,0xFF,0xDE,0xDE,0x80,0x80,0xFE,0xFE,0xDC,0x98,0xB2,0x84,0xCC,0xFF,
              0xDD,0x94,0xB6,0x80,0xC9,0xFF,0xF3,0xE3,0xDB,0x80,0x80,0xFB,0x84,0x86,0xAE,0xA0,
              0xB1,0xFF,0xC1,0x80,0xB6,0x90,0xD9,0xFF,0x9F,0x9C,0xB0,0x83,0x8F,0xFF,0xC9,0x80,
              0xB6,0x80,0xC9,0xFF,0xCD,0x84,0xB6,0x80,0xC1,0xFF,0xC1,0x80,0xBE,0x80,0xC1,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0x7F,0x7F,0xFF,0x7F,0x7F,0x7F,0x7F,0x7F,0x7F,0x7F,0xFF,0xFF,
              0xFF,0x7F,0x7F,0x7F,0xFF,0x7F,0x7F,0x7F,0x7F,0x7F,0xFF,0x7F,0x7F,0x7F,0x7F,0x7F,
              0x7F,0x7F,0x7F,0x7F,0x7F,0xFF,0xFF,0xFF,0xFF,0x7F,0x7F,0x7F,0x7F,0x7F,0x7F,0x7F,
              0xFF,0x7F,0x7F,0x7F,0x7F,0x7F,0x7F,0x7F,0xFF,0xFF,0x7F,0x7F,0x7F,0xFF,0xFF,0x7F,
              0x7F,0x7F,0x7F,0xFF,0x7F,0x7F,0x7F,0x7F,0x7F,0x7F,0x7F,0x7F,0x7F,0xFF,0x7F,0xFF,
              0x7F,0x7F,0x7F,0x7F,0xFF,0xFF,0x7F,0xFF,0xFF,0x7F,0x7F,0x7F,0xFF,0x7F,0x7F,0x7F,
              0x7F,0xFF,0xFF,0xFF,0xFF,0x7F,0x7F,0x3F,0xBF,0x7F,0x7F,0x7F,0x7F,0xFF,0x7F,0x7F,
              0x7F,0x7F,0x7F,0x7F,0xFF,0xFF,0x7F,0x7F,0x7F,0x7F,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xEC,0xE0,0xE5,0xE0,0xFC,0xEF,0xE0,0xE0,0xEB,0xE0,0xF4,0xFF,
              0xF0,0xE0,0xEF,0xE6,0xE6,0xEF,0xE0,0xE0,0xEF,0xE0,0xF0,0xEF,0xE0,0xE0,0xEB,0xEA,
              0xEE,0xEF,0xE0,0xE0,0xEB,0xEB,0xEF,0xFF,0xF0,0xE0,0xED,0xE4,0xF4,0xEF,0xE0,0xE0,
              0xFB,0xE0,0xE0,0xEF,0xEF,0xE0,0xE0,0xEF,0xFF,0xFC,0xFC,0xEF,0xE0,0xE0,0xEF,0xEF,
              0xE0,0xE0,0xF9,0xE4,0xEE,0xEF,0xE0,0xE0,0xEF,0xFE,0xFE,0xEF,0xE0,0xF1,0xFC,0xF1,
              0xE0,0xEF,0xE0,0xE0,0xF3,0xEC,0xE0,0xEF,0xF0,0xE0,0xEF,0xE0,0xF0,0xEF,0xE0,0xE0,
              0xED,0xE1,0xF3,0xFF,0xF0,0xE0,0xEF,0xE0,0xF0,0xEF,0xE0,0xE0,0xED,0xE0,0xF2,0xFF,
              0xF2,0xE3,0xE9,0xE8,0xE4,0xE7,0xEF,0xE0,0xE0,0xEF,0xE7,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xBF,0x3F,0x3F,0xBF,0xFF,0xFF,0x7F,0x3F,0xBF,0xBF,0xBF,
              0xFF,0xBF,0xBF,0xBF,0x3F,0x3F,0x7F,0xFF,0x7F,0x3F,0xBF,0x3F,0x7F,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xBF,0x3F,0x3F,0xBF,0xFF,0xFF,0x3F,0xFF,0x3F,0xFF,0x3F,0xFF,0x3F,
              0x3F,0xBF,0x3F,0x3F,0xBF,0x6F,0x2F,0xAF,0x0F,0x1F,0xFF,0x7F,0x3F,0xBF,0xBF,0xBF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xF3,0xF7,0xF0,0xF0,0xF7,0xF3,0xFF,0xFC,0xF8,0xFA,0xF8,0xFC,
              0xFF,0xFD,0xF8,0xF8,0xFA,0xFA,0xFF,0xFB,0xE0,0xE0,0xFB,0xFB,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xF7,0xF0,0xF0,0xF7,0xFF,0xFB,0xF8,0xF9,0xF8,0xF9,0xFC,0xFF,0xFD,
              0xF8,0xFA,0xF8,0xFC,0xFF,0xFC,0xF8,0xFB,0xFC,0xF8,0xFB,0xFC,0xF8,0xFA,0xF8,0xFC,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x9F,0xDF,
              0x5F,0x1F,0x3F,0xFF,0xDF,0x1F,0x1F,0xDF,0xFF,0xFF,0xFF,0x9F,0x1F,0x7F,0xFF,0xFF,
              0x9F,0xDF,0xDF,0x1F,0x3F,0xFF,0x3F,0x1F,0xDF,0x1F,0x3F,0xFF,0xFF,0x9F,0x1F,0x7F,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFC,0xF8,
              0xFA,0xFA,0xF9,0xF9,0xFB,0xF8,0xF8,0xFB,0xF9,0xFF,0xF3,0xF3,0xF6,0xF0,0xF1,0xFF,
              0xF0,0xF0,0xF5,0xF4,0xF6,0xFF,0xF8,0xF0,0xF6,0xF2,0xFB,0xFF,0xF3,0xF3,0xF6,0xF0,
              0xF1,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
              0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

class ST7567_LCD:
    def __init__(self, RST=24, A0=23, max_speed_hz=1953000, spi_port=0, spi_device=0):
        self.RST = RST
        self.A0 = A0
        self.max_speed_hz = max_speed_hz
        self.spi_port = spi_port
        self.spi_device = spi_device
        self.is_initialized = False

    def __del__(self):
        self.close()

    def initialize(self):
        # Setup GPIO pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.RST, GPIO.OUT)
        GPIO.setup(self.A0, GPIO.OUT)

        # Open SPI device
        self.spi = spidev.SpiDev()
        self.spi.open(self.spi_device, self.spi_port)
        self.spi.max_speed_hz = self.max_speed_hz

        # First reset the display
        GPIO.output(self.A0, 0)

        GPIO.output(self.RST, 1)
        sleep(0.3)
        GPIO.output(self.RST, 0)
        sleep(0.3)
        GPIO.output(self.RST, 1)

        # Send init sequence
        self.spi.xfer2([ST7567_BIAS_SELECT_1OVER9,
                        ST7567_SEG_DIRECTION_REVERSE,
                        ST7567_INVERSE_DISPLAY_OFF,
                        ST7567_COM_DIRECTION_NORMAL,
                        ST7567_SET_BOOSTER, 0,
                        ST7567_POWER_CONTROL | 0b111, # VB on, VR on, VF on
                        ST7567_REGULATION_RATIO | 0b110, # RR2 on, RR1 on, RR0 off
                        ST7567_SET_CONTRAST, 8,
                        ST7567_SET_START_LINE,
                        ST7567_DISPLAY_ON])

        self.is_initialized = True
    
    def close(self):
        self.spi.xfer2([ST7567_DISPLAY_OFF,
                        ST7567_ALL_PIXEL_ON])
        sleep(0.25)
        self.spi.xfer2([ST7567_REGULATION_RATIO,
                        ST7567_POWER_CONTROL])
        self.spi.close()
        self.is_initialized = False

    def clear(self, set_zeros=True):
        assert self.is_initialized, 'Trying to clear uninitialized display'
        if set_zeros:
            self.show_image_raw([0x00] * 1024)
        else:
            self.show_image_raw([0xFF] * 1024)
    
    def invert(self, on=True):
        assert self.is_initialized, 'Trying to invert uninitialized display'
        if on:
            self.spi.xfer([ST7567_INVERSE_DISPLAY_ON])
        else:
            self.spi.xfer([ST7567_INVERSE_DISPLAY_OFF])

    def show_image_raw(self, image):
        assert self.is_initialized, 'Trying to show image on uninitialized display'
        self.spi.xfer([ST7567_SET_START_LINE])
        for page in range(8):
            # Write page adress
            self.spi.xfer([ST7567_SET_PAGE_ADDRESS | page])
            # Set column adress
            self._set_column_adress(0)

            # Data mode on
            GPIO.output(self.A0, 1)
            self.spi.xfer2(image[page*128:(page+1)*128])
            GPIO.output(self.A0, 0)
    
    def show_image_binary(self, image):
        assert isinstance(image, np.ndarray), 'Image must be of type numpy ndarray'
        assert image.dtype == np.bool, 'Data needs to be binary'
        assert image.shape == (64, 128), 'Wrong image dimension. Must fit display dimensions (64 x 128)'
        

        # Convert binary image to raw and show
        # Note: np.packbits does not offer the bitorder parameter --> use flip
        self.show_image_raw(np.packbits(np.flip(image.T.reshape(128,8,8), axis=2), axis=2).T.flatten().tolist())
    
    def set_contrast(self, contrast):
        assert self.is_initialized, 'Trying to set contrast of uninitialized display'
        assert 0 <= contrast < 64, 'Contrast level should be in the range 0-63'
        self.spi.xfer2([ST7567_SET_CONTRAST, 
                        contrast])

    def _set_column_adress(self, addr):
        addr += 4
        self.spi.xfer2([(ST7567_SET_COLUMN_ADDRESS_MSB | addr >> 4), 
                        (ST7567_SET_COLUMN_ADDRESS_LSB & addr)])


if __name__ == '__main__':
    from time import sleep
    print('Running ST7567 unit test')

    print('Initializing display with default pinout (RST=24, A0=23)')
    LCD = ST7567_LCD()
    LCD.initialize()
    #sleep(2)

    print('Clearing display - zeros')
    LCD.clear()
    sleep(2)
    print('Clearing display - ones')
    LCD.clear(set_zeros=False)
    sleep(2)

    print('Showing binary image - horizontal line')
    LCD.show_image_binary(np.array([0]*128*31 + [1]*128*2 + [0]*128*31).reshape(64, 128).astype(np.bool))
    sleep(2)

    print('Showing binary image - diagonal line')
    diag_image = np.diag([1]*128)[0:64, :]
    LCD.show_image_binary(diag_image.astype(np.bool))
    sleep(2)

    print('Display test image')
    LCD.show_image_raw(image=test_image)
    sleep(2)

    print('Inverting contrast ON')
    LCD.invert()
    sleep(2)
    print('Inverting contrast OFF')
    LCD.invert(False)
    sleep(2)

    print('Set contrast level')
    for i in range(0,20):
        print(i)
        LCD.set_contrast(i)
        sleep(1)

    print('Done')