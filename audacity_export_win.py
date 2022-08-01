#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Make sure Audacity is running first and that mod-script-pipe is enabled before running this script.

# Create a shortcut: Set the target to %systemroot%\System32\cmd.exe /c "python C:\Users\MyUsername\Documents\audacity_export_win.py"

import os
import sys
from datetime import datetime
import shutil

# Sekhar Audacity Export Variables Start
# output_dir = 'C:\Users'
output_dir = '/Users/reedz/Desktop/audacity_test/'
server_dir = '/Users/reedz/Desktop/audacity_test/server/'
# Sekhar Audacity Export Variables End

# Init

if sys.platform == 'win32':
    print("pipe-test.py, running on windows")
    TONAME = '\\\\.\\pipe\\ToSrvPipe'
    FROMNAME = '\\\\.\\pipe\\FromSrvPipe'
    EOL = '\r\n\0'
else:
    print("pipe-test.py, running on linux or mac")
    TONAME = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
    FROMNAME = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
    EOL = '\n'

print("Write to  \"" + TONAME +"\"")
if not os.path.exists(TONAME):
    print(" ..does not exist.  Ensure Audacity is running with mod-script-pipe.")
    sys.exit()

print("Read from \"" + FROMNAME +"\"")
if not os.path.exists(FROMNAME):
    print(" ..does not exist.  Ensure Audacity is running with mod-script-pipe.")
    sys.exit()

print("-- Both pipes exist.  Good.")

TOFILE = open(TONAME, 'w')
print("-- File to write to has been opened")
FROMFILE = open(FROMNAME, 'rt')
print("-- File to read from has now been opened too\r\n")


def send_command(command):
    """Send a single command."""
    print("Send: >>> \n"+command)
    TOFILE.write(command + EOL)
    TOFILE.flush()

def get_response():
    """Return the command response."""
    result = ''
    line = ''
    while True:
        result += line
        line = FROMFILE.readline()
        if line == '\n' and len(result) > 0:
            break
    return result

def do_command(command):
    """Send one command, and return the response."""
    send_command(command)
    response = get_response()
    print("Rcvd: <<< \n" + response)
    return response

def quick_test():
    """Example list of commands."""
    do_command('Help: Command=Help')
    do_command('Help: Command="GetInfo"')
    #do_command('SetPreference: Name=GUI/Theme Value=classic Reload=1')

# End Init

# Sekhar Audacity Export Start

if datetime.today().hour < 13:
    session = "S2"
else:
    session = "S3"
    
top_track_output = output_dir + datetime.today().strftime('%y%m%d') +'-DKR-'+ session + '-Lama.mp3'
botton_track_output = output_dir + datetime.today().strftime('%y%m%d') +'-DKR-'+ session + '-Chi.mp3'

# Set Export Format
do_command('SetPreference: Name="FileFormats/MP3RateModeChoice" Value="CBR" Reload=1')
do_command('SetPreference: Name="FileFormats/MP3Bitrate" Value="128" Reload=1')

# Select Track 1 - Top , Then Normalize / Export
do_command('SelectTracks:Mode="Set" Track="0" TrackCount="0.5"')
do_command('Normalize:ApplyGain="1" PeakLevel="-1" RemoveDcOffset="1"')
do_command(f'Export2:Filename="{top_track_output}" NumChannels=1')

# Select Track 1 - Bottom , Then Normalize / Export
do_command('SelectTracks:Mode="Set" Track="0.5" TrackCount="0.5"')
do_command('Normalize:ApplyGain="1" PeakLevel="-1" RemoveDcOffset="1"')
do_command(f'Export2:Filename="{botton_track_output}" NumChannels=1')



'''
if sys.platform == 'win32':
    # scan available Wifi networks
    os.system('cmd /c "netsh wlan show networks"')
    # input Wifi name
    name_of_router = input('Enter Name/SSID of the Wifi Network you wish to connect to: ')
    # connect to the given wifi network
    os.system(f'''cmd /c "netsh wlan connect name={name_of_router}"''')
    print("If you're not yet connected, try connecting to a previously connected SSID again!")
'''


# Copy to Server
shutil.copy(top_track_output, server_dir)
shutil.copy(botton_track_output, server_dir)