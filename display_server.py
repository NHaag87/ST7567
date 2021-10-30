import falcon
import json
import numpy as np
from ST7567 import ST7567_LCD


class lcd_display_server:

    def __init__(self, lcd):
        self.lcd = lcd

    def _exception_response(request):
        def requester(self, req, resp):
            try:
               request(self, req, resp)
            except Exception as error:
                resp.text = '\n'.join(['Error:', 
                                        '', 
                                        f'{type(error).__name__}: {str(error)}'])
                resp.status = falcon.HTTP_400
        return requester

    @_exception_response
    def on_get_help(self, req, resp):
        resp.text = '\n'.join(['Commands:', 
                               '', 
                               'set_image_raw - POST with parameter \'image\' as list of 1024 uint8s',
                               'set_image_binary - POST with parameter \'image\' as list of 64*128 bools',
                               'clear_ones - GET',
                               'clear_zeros - GET',
                               'invert_on - GET',
                               'invert_off - GET'])
        resp.status = falcon.HTTP_200
    
    @_exception_response
    def on_post_set_image_raw(self, req, resp):
        assert 'image' in req.media, 'Image not found'
        assert len(req.media['image']) == 1024, 'Incorrect image size or format'
        
        image = req.media['image']

        image = np.array([int(n) for n in image], dtype=np.uint8).tolist()
        self.lcd.show_image_raw(image)

        resp.text = 'OK'

        resp.status = falcon.HTTP_200
    
    @_exception_response
    def on_post_set_image_binary(self, req, resp):
        assert 'image' in req.media, 'Image not found'
        assert len(req.media['image']) == 128*64, 'Incorrect image size or format'
        
        image = req.media['image']

        image = np.array([int(n) for n in image], dtype=np.bool).reshape(64, 128)
        self.lcd.show_image_binary(image)

        resp.text = 'OK'

        resp.status = falcon.HTTP_200


    @_exception_response
    def on_get_clear_ones(self, req, resp):
        self.lcd.clear(set_zeros=False)

        resp.text = 'OK'

        resp.status = falcon.HTTP_200

    @_exception_response
    def on_get_clear_zeros(self, req, resp):
        self.lcd.clear(set_zeros=True)

        resp.text = 'OK'

        resp.status = falcon.HTTP_200
    
    @_exception_response
    def on_get_invert_on(self, req, resp):
        self.lcd.invert(True)

        resp.text = 'OK'

        resp.status = falcon.HTTP_200
    
    @_exception_response
    def on_get_invert_off(self, req, resp):
        self.lcd.invert(False)

        resp.text = 'OK'

        resp.status = falcon.HTTP_200


# Setup falcon app
app = falcon.App()

# Initialize LCD display
lcd = ST7567_LCD()
lcd.initialize()
lcd.clear()

# Initialize falcon server
display_server = lcd_display_server(lcd)
app.add_route('/help', display_server, suffix='help')
app.add_route('/set_image_raw', display_server, suffix='set_image_raw')
app.add_route('/set_image_binary', display_server, suffix='set_image_binary')
app.add_route('/clear_ones', display_server, suffix='clear_ones')
app.add_route('/clear_zeros', display_server, suffix='clear_zeros')
app.add_route('/invert_on', display_server, suffix='invert_on')
app.add_route('/invert_off', display_server, suffix='invert_off')


