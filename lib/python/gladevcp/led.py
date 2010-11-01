# vim: sts=4 sw=4 et
import gtk
import gobject
import cairo
import math
import gtk.glade

# This creates the custom LED widget

from hal_widgets import _HalSensitiveBase

class HAL_LED(gtk.DrawingArea, _HalSensitiveBase):
    __gtype_name__ = 'HAL_LED'
    __gproperties__ = {
        'is_on' : ( gobject.TYPE_BOOLEAN, 'Is on', 'How to display LED in editor',
                    False, gobject.PARAM_READWRITE | gobject.PARAM_CONSTRUCT),
        'led_shape' : ( gobject.TYPE_INT, 'Shape', '0: round 1:oval 2:square',
                    0, 2, 0, gobject.PARAM_READWRITE | gobject.PARAM_CONSTRUCT),
        'led_size'  : ( gobject.TYPE_INT, 'Size', 'size of LED',
                    5, 30, 10, gobject.PARAM_READWRITE | gobject.PARAM_CONSTRUCT),
        'led_blink_rate' : ( gobject.TYPE_INT, 'Blink rate',  'Led blink rate (ms)',
                    100, 1000, 500, gobject.PARAM_READWRITE),
        'pick_color_on'  : ( gtk.gdk.Color.__gtype__, 'Pick on color',  "",
                    gobject.PARAM_READWRITE),
        'pick_color_off' : ( gtk.gdk.Color.__gtype__, 'Pick off color', "",
                        gobject.PARAM_READWRITE),
        'on_color'  : ( gobject.TYPE_STRING, 'LED On color', 'Use any valid Gdk color',
                        "red", gobject.PARAM_READWRITE | gobject.PARAM_CONSTRUCT),
        'off_color' : ( gobject.TYPE_STRING, 'LED OFF color', 'Use any valid Gdk color or "dark"',
                        "dark", gobject.PARAM_READWRITE | gobject.PARAM_CONSTRUCT)
    }
    __gproperties = __gproperties__

    def post_create(self, obj, reason):
                print "\nhola\n"

    def __init__(self):
        print "LED init"
        super(HAL_LED, self).__init__()
        self._dia = 10
        self._blink_active = False
        self._blink_state = False
        self._blink_magic = 0
        self.set_size_request(25, 25)
        self.connect("expose-event", self.expose)

        self.led_blink_rate = None
        self.pick_color_on = self.pick_color_off = None
        self.on_color = 'red'
        self.off_color = 'dark'

        self.set_color('on', self.on_color)
        self.set_color('off', self.on_color)

    # This method draws our widget
    # depending on self.state, self.blink_active, self.blink_state and the sensitive state of the parent
    # sets the fill as the on or off colour.
    def expose(self, widget, event):
        cr = widget.window.cairo_create()
        set_source_color_alpha = lambda c,a=1: cr.set_source_rgba(c.red_float, c.green_float, c.blue_float, a)
        sensitive = self.flags() & gtk.PARENT_SENSITIVE
        if not sensitive: alpha = .3
        else: alpha = 1
        cr.set_line_width(3)
        cr.set_source_rgba(0, 0, 0, alpha)
        # square led
        if self.led_shape == 2:
            self.set_size_request(self._dia*2+5, self._dia*2+5)
            w = self.allocation.width
            h = self.allocation.height
            cr.translate(w/2, h/2)
            cr.rectangle(-self._dia, -self._dia, self._dia*2,self._dia*2)
        # oval led
        elif self.led_shape == 1:
            self.set_size_request(self._dia*2+5, self._dia*2+5)
            w = self.allocation.width
            h = self.allocation.height
            cr.translate(w/2, h/2)
            cr.scale( 1, 0.7);
            cr.arc(0, 0, self._dia, 0, 2*math.pi)
        # round led
        else:            
            self.set_size_request(self._dia*2+5, self._dia*2+5)           
            w = self.allocation.width
            h = self.allocation.height
            cr.translate(w/2, h/2)
            lg2 = cairo.RadialGradient(1., 1., 1., 0, 1, self._dia*2)
            cr.arc(0, 0, self._dia, 0, 2*math.pi)
            cr.mask(lg2)

        cr.stroke_preserve()        
        if self.is_on:
            if self._blink_active == False or self._blink_active == True and self._blink_state == True:
                set_source_color_alpha(self._on_color, alpha)
            else:
                set_source_color_alpha(self._off_color, alpha)
        else:
            set_source_color_alpha(self._off_color, alpha)
        cr.fill()    
        return False
      
    # This sets the LED on or off color
    # and then redraws it
    # Usage: ledname.set_active(True) 
    def set_active(self, data):
        self.is_on = data
        self.queue_draw()

    def set_sensitive(self, data ):
        self.set_active(data)

    #FIXME the gobject timers are never explicly destroyed
    def set_blink_rate(self,rate):
        if rate == 0:
            self._blink_active = False
        else:
            self._blink_active = True
            self._blink_magic += 1
            self._blink_timer = gobject.timeout_add(rate, self.blink, self._blink_magic)

    def blink(self, magic=None):
        if not self._blink_active:
            return False
        if magic is not None and self._blink_magic != magic:
            return False
        if self._blink_state == True:
            self._blink_state = False
        else: self._blink_state = True
        self.queue_draw()
        return True # keep running this event

    # This allows setting of the on and off colour
    # red,green and blue are float numbers beteen 0 and 1
    # if color = None uses colorname. only a few names supported
    # Usage: ledname.set_color("off",[r,g,b],"colorname")
    def set_color(self, state, color):
        if isinstance(color, gtk.gdk.Color):
            pass
        elif color != 'dark':
            color = gtk.gdk.Color(color)
        else:
            r = 0.4 * self._on_color.red_float
            g = 0.4 * self._on_color.green_float
            b = 0.4 * self._on_color.blue_float
            color = gtk.gdk.Color(r, g, b)
        if state == "off":
            self._off_color = color
        elif state == "on":
            self._on_color = color

        if state == 'on' and getattr(self, 'off_color') == 'dark':
            self.set_color('off', 'dark')

    # This alows setting the diameter of the LED
    # Usage: ledname.set_dia(10)
    def set_dia(self, dia):
        self._dia = dia
        self.queue_draw()

    # This sets the shape round oval or square
    def set_shape(self, shape):
        self.led_shape = shape
        self.queue_draw()

    def do_get_property(self, property):
        name = property.name.replace('-', '_')
        if name == 'led_size':
            return self._dia
        elif name in self.__gproperties.keys():
            return getattr(self, name)
        else:
            raise AttributeError('unknown property %s' % property.name)

    def do_set_property(self, property, value):
        name = property.name.replace('-', '_')
        if name in ['on_color', 'off_color']:
            mode = name.split('_')[0]
            if getattr(self, 'pick_color_%s' % mode, None):
                return False
            try:
                self.set_color(mode, value)
            except:
                print "Invalid %s color value: %s" % (mode, value)
                return False
        elif name in ['pick_color_on', 'pick_color_off']:
            mode = name.split('_')[-1]
            if not value:
                return False
            self.set_color(mode, value)
        elif name == 'led_blink_rate':
            self.set_blink_rate(value)

        if name == 'led_size':
            self._dia = value
        elif name in self.__gproperties.keys():
            setattr(self, name, value)
        else:
            raise AttributeError('unknown property %s' % property.name)
        self.queue_draw()
        return True

    def _hal_init(self):
        _HalSensitiveBase._hal_init(self)
        self.set_color('on',  self.pick_color_on or self.on_color)
        self.set_color('off', self.pick_color_off or self.off_color)
        if self.led_blink_rate:
            self.set_blink_rate(self.led_blink_rate)
