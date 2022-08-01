#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Make sure Audacity is running first and that mod-script-pipe is enabled before running this script.

import os
import sys
import shutil
from datetime import datetime
from appscript import *
from audacity_functions import *
from audacity_config import *
# import pyautogui

# pyautogui.alert('Just a notification', "Title")  # always returns "OK"

# from tkinter import messagebox  # Python 3

# messagebox.showinfo("Title", "message")

# Sekhar Audacity Export Variables Start
# output_dir = 'C:\Users'

# Sekhar Audacity Export Variables End


# Sekhar Audacity Export Start

if datetime.today().hour < 13:
    session = "S2"
else:
    session = "S3"
    
track_output = output_dir + datetime.today().strftime('%y%m%d') +'-DKR-'+ session + '-En.mp3'


# Set Export Format
do_command('SetPreference: Name="FileFormats/MP3RateModeChoice" Value="CBR" Reload=1')
do_command('SetPreference: Name="FileFormats/MP3Bitrate" Value="128" Reload=1')

# Select Track 1 - Top , Then Normalize / Export
do_command('SelectTracks:Mode="Set" Track="0" TrackCount="1"')
do_command('Normalize:ApplyGain="1" PeakLevel="-1" RemoveDcOffset="1"')
do_command(f'Export2:Filename="{track_output}" NumChannels=1')

'''
if sys.platform == 'win32':
    # scan available Wifi networks
    os.system('cmd /c "netsh wlan show networks"')
    # input Wifi name
    name_of_router = input('Enter Name/SSID of the Wifi Network you wish to connect to: ')
    # connect to the given wifi network
    os.system(f'cmd /c "netsh wlan connect name="{name_of_router}"')
    print("If you're not yet connected, try connecting to a previously connected SSID again!")
'''


# Copy to Server
shutil.copy(track_output, server_dir)

# Reveal
app("Finder").reveal(mactypes.Alias(track_output).alias)
app("Finder").reveal(mactypes.Alias(server_dir).alias)