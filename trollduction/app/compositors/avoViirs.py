import mpop.imageo.geo_image as geo_image
#from PIL import Image
from pydecorate import DecoratorAGG
import aggdraw
from trollimage.colormap import rdgy
from trollimage.colormap import Colormap
from trollsched.satpass import Pass
from pprint import pprint
from mpop.projector import get_area_def

def avoir(self):
    """Make a black and white image of the IR 10.8um channel (320m).
       Modeled after mpop.instruments.viirs.ir108
    """
    self.check_channels("M15")
    data = self["M15"].data
    range = (-65 + 273.15, 35 + 273.15)
    img = geo_image.GeoImage((data, data, data),
                                self.area,
                                self.time_slot,
                                fill_value=None,
                                mode="RGB",
                                crange=(range, range, range))
    # clouds should be white
    img.enhance(inverse=True)

    img.add_overlay(color=(218,165,32))

    return img

avoir.prerequisites = set(["M15"])


def avoash(self):
    """Make BTD composite.
    """
    self.check_channels('M15', 'M16')
    img = geo_image.GeoImage(self["M15"].data - self["M16"].data,
                             self.area,
                             self.time_slot,
                             fill_value=0,
                             mode="L",
                             crange=(-6, 5))
    img.colorize(rdgy)
    return img

avoash.prerequisites = set(["M15", "M16"])


viirs = [avoir, avoash]
