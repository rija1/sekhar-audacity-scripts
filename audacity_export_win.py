#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Make sure Audacity is running first and that mod-script-pipe is enabled before running this script.

# Create a shortcut: Set the target to %systemroot%\System32\cmd.exe /c "python C:\Users\MyUsername\Documents\audacity_export_win.py"

import os
import sys
from datetime import datetime
import shutil
from audacity_functions import *
from audacity_config import *

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

# Copy to Server
shutil.copy(top_track_output, server_dir)
shutil.copy(botton_track_output, server_dir)