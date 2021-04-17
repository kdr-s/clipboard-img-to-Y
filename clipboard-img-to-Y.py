from PIL import ImageGrab, ImageChops, Image
from time import sleep
from ctypes import windll
import numpy as np

last_im = Image.new("RGB", (512, 512), (128, 128, 128))
Ctrl = 0x11

def isPressed(key):
    return(bool(windll.user32.GetAsyncKeyState(key)&0x8000))

while True:
    im = ImageGrab.grabclipboard()
    if isinstance(im, Image.Image):
        im = im.convert('RGB')
        # ２つの画像の同一かどうか
        if ImageChops.difference(im, last_im).getbbox() != None:
            last_im = im
            if isPressed(Ctrl):
                # lumi_im = im.convert("L")
                array = np.asarray(im, dtype='float')
                array = (array/255)**2.2
                # array = array[:][:][0]*0.2126; array = array[:][:][1]*0.7152;  array = array[:][:][2]*0.0722; 
                array = np.sum(array*np.array([[[0.2126,0.7152,0.0722]]]), axis=2)
                array = (array**(1/2.2))*255
                array = np.round(array).astype('uint8')
                lumi_im = Image.fromarray(array)
                lumi_im.show()
    sleep(1)
