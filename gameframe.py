#! /usr/bin/python

from os import listdir
from os.path import isfile, join, isdir
import sys, os, time, re, configparser, numbers, signal

import unicornhathd
from PIL import Image

def main(args):
    unicornhathd.rotation(0)
    unicornhathd.brightness(0.6)

    signal.signal(signal.SIGTERM, sig_handler)

    if len(args) == 1:
        onlyfiles = [f for f in listdir('.') if is_dir(f)]
        try:
            for file in sorted(onlyfiles):
                for count in [1,2,3,4,5,6,7,8,9,10]:
                    if file != '00system':
                        process_dir(file)
        except KeyboardInterrupt:
            shutdown()
    else:
        try:
            while True:
                process_dir(args[1])
        except KeyboardInterrupt:
            shutdown()
            sys.exit(15)

def sig_handler(signal, frame):
    print "Caught signal"
    shutdown()

def shutdown():
    unicornhathd.off()
    sys.exit(15)


def process_dir(dirname):

    onlyfiles = [f for f in listdir(dirname) if is_image(join(dirname,f))]

    config = configparser.ConfigParser()
    try:
        bob = config.read(join(dirname,"config.ini"))
    except:
        print "No config.ini"


    hold_ms = int(config["animation"]["hold"])

    unicornhathd.rotation(0)
    unicornhathd.brightness(0.6)

    sleep_time = round(hold_ms/100,2)/10
    sleep_time = 0.1

    for filename in sorted(onlyfiles, key=sort_leading_num):
       display(join(dirname, filename))

       time.sleep(sleep_time)

def sort_leading_num(key):
    m =  re.search(r"^([0-9]*)\.",key)
    if m:
        return int(m.group(1))
    return key

def display(filename):
    img = Image.open(filename)
    width, height = unicornhathd.get_shape()

    for o_x in range(int(img.size[0] / width)):
        for o_y in range(int(img.size[1] / height)):
            valid = False
            for x in range(width):
                for y in range(height):
                    pixel = img.getpixel(((o_x) + y, (o_y * height) + x))
                    r, g, b = int(pixel[0]), int(pixel[1]), int(pixel[2])
                    if r or g or b:
                        valid = True
                    unicornhathd.set_pixel(x,y,r,g,b)
            if valid:
                unicornhathd.show()

def is_dir(filename):
    if not isdir(filename):
        return False
    return True

def is_image(filename):
    if not isfile(filename):
        return False
    if re.search(r"bmp",filename):
        return True
    return False

main(sys.argv)
