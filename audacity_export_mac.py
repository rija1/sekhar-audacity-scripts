#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Make sure Audacity is running first and that mod-script-pipe is enabled before running this script.

import os
import sys
import shutil
from datetime import datetime
from appscript import *
from audacity_init import *
from audacity_config import *

# Sekhar Audacity Export Start
track_output = output_dir + datetime.today().strftime('%y%m%d') + '-DKR-' + year + '-' + session + '-En.mp3'

# Select Track 1 - Top , Then Normalize / Export
do_command('SelectTracks:Mode="Set" Track="0" TrackCount="1"')
do_command('Normalize:ApplyGain="1" PeakLevel="-1" RemoveDcOffset="1"')
do_command(f'Export2:Filename="{track_output}" NumChannels=1')

# Copy to Server
shutil.copy(track_output, server_dir)

# Reveal
app("Finder").reveal(mactypes.Alias(track_output).alias)
app("Finder").reveal(mactypes.Alias(server_dir).alias)