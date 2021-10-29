# ST7567
A small python driver to operate ST7567 based displays via REST interface. The project just started, so don't expect the a full fledged version ;)

## Hardware
I used the following displays:
* https://www.buydisplay.com/1-54-inch-black-128x64-graphic-lcd-display-module-spi-for-arduino
* https://www.buydisplay.com/1-54-inch-blue-128x64-graphic-lcd-display-module-spi-for-arduino-1
* https://www.buydisplay.com/1-54-inch-white-128x64-graphic-lcd-display-module-spi-for-arduino

Basically any 128x64 graphical dot display equipped with a ST7567 controller should work (hopefully ;))

## MWE
    import ST7567

    LCD = ST7567.ST7567_LCD(RST=24, A0=23)
    LCD.initialize()
    LCD.clear()
    LCD.show_image_raw(ST7567.test_image)

## Wiring
TODO

## REST API
The module is equipped with an additional falcon based REST API that allows you to control the display remotely via HTTP GET/POST requests. 
