#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# Make sure Audacity is running first and that mod-script-pipe is enabled before running this script.

import os
import sys
import shutil
from datetime import datetime
from appscript import *

from audacity_init import *
from audacity_config import *

from tkinter import *

root = Tk()
root.title('Sekhar Audacity Export')
root.geometry("500x360")

var = IntVar()

label1 = Label(root,text="Export options",font=("Arial", 16)).place(x=10,y=10)

def sel():
    # global check1
    # global check2
    # global check3
    if export_radio.get() == 1:
        check1.config(state='active')
        check2.config(state='active')
        check3.config(state='disabled')
    if export_radio.get() == 2:
        check1.config(state='active')
        check2.config(state='disabled')
        check3.config(state='disabled')
    if export_radio.get() == 3:
        check1.config(state='disabled')
        check2.config(state='disabled')
        check3.config(state='active')

def launchExport():
    
    statusLabel.config(text="Working.",fg='#4b6efa')
    
    exportPath = entryExportPath.get()
    copyPath = entryCopyPath.get()
    
    # Export Lama/Chi
    if export_radio.get() == 1:
        top_track_output = output_dir + datetime.today().strftime('%y%m%d') + '-DKR-' + year + '-' + session + '-Lama.mp3'
        bottom_track_output = output_dir + datetime.today().strftime('%y%m%d') + '-DKR-' + year + '-' + session + '-Chi.mp3'

        # Select Track 1 - Top , Then Normalize / Export
        do_command('SelectTracks:Mode="Set" Track="0" TrackCount="0.5"')
        do_command('Normalize:ApplyGain="1" PeakLevel="-1" RemoveDcOffset="1"')
        do_command(f'Export2:Filename="{top_track_output}" NumChannels=1')

        # Select Track 1 - Bottom , Then Normalize / Export
        do_command('SelectTracks:Mode="Set" Track="0.5" TrackCount="0.5"')
        do_command('Normalize:ApplyGain="1" PeakLevel="-1" RemoveDcOffset="1"')
        do_command(f'Export2:Filename="{bottom_track_output}" NumChannels=1')
        
        # If copy Lama
        if copy_lama.get() == 1 :
            shutil.copy(top_track_output, server_dir)
        # If copy Chi
        if copy_chi.get() == 1 :
            shutil.copy(bottom_track_output, server_dir)
        
    # Export Lama only
    if export_radio.get() == 2:
        # Sekhar Audacity Export Start
        track_output = exportPath + datetime.today().strftime('%y%m%d') + '-DKR-' + year + '-' + session + '-Lama.mp3'

        # Select Track 1 - Top , Then Normalize / Export
        do_command('SelectTracks:Mode="Set" Track="0" TrackCount="1"')
        do_command('Normalize:ApplyGain="1" PeakLevel="-1" RemoveDcOffset="1"')
        do_command(f'Export2:Filename="{track_output}" NumChannels=1')
        
        # If copy Lama
        if copy_lama.get() == 1 :
            shutil.copy(track_output, copyPath)
        
    # Export Eng only
    if export_radio.get() == 3:
        # Sekhar Audacity Export Start
        track_output = exportPath + datetime.today().strftime('%y%m%d') + '-DKR-' + year + '-' + session + '-En.mp3'

        # Select Track 1 - Top , Then Normalize / Export
        do_command('SelectTracks:Mode="Set" Track="0" TrackCount="1"')
        do_command('Normalize:ApplyGain="1" PeakLevel="-1" RemoveDcOffset="1"')
        do_command(f'Export2:Filename="{track_output}" NumChannels=1')
        
        # If copy En
        if copy_en.get() == 1 :
            shutil.copy(track_output, copyPath)

    # Reveal
    # app("Finder").reveal(mactypes.Alias("/Users/reedz/Desktop/1930457_32256137852_4792_n.jpeg").alias)
    reveal_track# _output = track_output
#     reveal_copyPath = copyPath
#
#     app("Finder").reveal(mactypes.Alias(reveal_track_output).alias)
#     app("Finder").reveal(mactypes.Alias(reveal_copyPath).alias)
    root.destroy()

export_radio = IntVar()
rbutton1 = Radiobutton(root, text="Export Lama/Chi", variable=export_radio, value=1,command=sel);
rbutton1.place(x=10,y=40)
rbutton1.select()
rbutton2 = Radiobutton(root, text="Export Lama only", variable=export_radio, value=2,command=sel)
rbutton2.place(x=10,y=70)
rbutton3 = Radiobutton(root, text="Export Eng only", variable=export_radio, value=3,command=sel)
rbutton3.place(x=10,y=100)

labelExportPath = Label(root,text="Export Path",font=("Arial", 13)).place(x=15,y=140)

entryExportPath = Entry(root)
entryExportPath.place(x=100,y=137)
entryExportPath.insert(0, output_dir)

label2 = Label(root,text="Copy to server",font=("Arial", 16)).place(x=10,y=180)

labelCopyPath = Label(root,text="Export Path",font=("Arial", 13)).place(x=15,y=210)

entryCopyPath = Entry(root)
entryCopyPath.place(x=100,y=207)
entryCopyPath.insert(0, server_dir)

copy_lama = IntVar(value=1)
check1 = Checkbutton(root, variable=copy_lama, text ="Lama");
check1.place(x=10,y=250)
check1.select()

copy_chi = IntVar(value=1)
check2 = Checkbutton(root, variable=copy_chi, text ="Chi");
check2.place(x=87,y=250)
check2.select()

copy_en = IntVar(value=1)
check3 = Checkbutton(root, variable=copy_en, text ="Eng");
check3.place(x=150,y=250)
check3.config(state='disabled')

launchButton = Button(root, text="Start Export", command=launchExport)
launchButton.place(x=10,y=300)

statusLabel = Label(root,text="Ready.",fg='#63c266', font=("Arial", 13))
statusLabel.place(x=130,y=305)

root.mainloop()