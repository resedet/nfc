#!/usr/bin/env python3
#
# Copyright (c) 2020, Ryota Sakaguchi.
# All rights reserved.
#
#
# $Id: read4digits.py, 2020/09/24 19:52:26
#

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import time
import datetime
import subprocess
import pygame.mixer
import nfc
# https://nfcpy.readthedocs.io/en/latest/overview.html

today = subprocess.getoutput('date +%y%m%d')
PATH = './log/' + today + '.log'

def sound(mp3):
    pygame.mixer.init()
    pygame.mixer.music.load(mp3)
    pygame.mixer.music.play(1)
    time.sleep(1)
    pygame.mixer.music.stop()

clf = nfc.ContactlessFrontend('usb')
print('\033[32m*** waiting for a tag ***\033[0m', file=sys.stderr)

while True:
    target = clf.sense(nfc.clf.RemoteTarget("212F"), interval=1.0)

    while target:
        tag = nfc.tag.activate(clf, target)

        sc = nfc.tag.tt3.ServiceCode(64, 0x0b)
        bc = nfc.tag.tt3.BlockCode(0, service=0)

        try:
            data = tag.read_without_encryption([sc], [bc])
            s = str(datetime.datetime.now()) + data[6:10].decode()
            print(s)
            print(data[6:10].decode(), file=sys.stderr)
            sound("chime.mp3")
            print('\033[32m*** waiting for a tag ***\033[0m', file=sys.stderr)
            break
        
        except nfc.tag.tt3.Type3TagCommandError:
            print('\033[31m*** please try again ***\033[0m', file=sys.stderr)
            sound("buzzer.mp3")
            break
