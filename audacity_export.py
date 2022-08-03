#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# Make sure Audacity is running first and that mod-script-pipe is enabled before running this script.

import os
import sys
import shutil
from datetime import datetime
from appscript import *
from audacity_config import *
from tkinter import *
from tkinter import messagebox
import os.path
from os import path

# Functions - Start

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
        
def addMonoTrack():
    do_command('NewMonoTrack:')
    
def addStereoTrack():
    do_command('NewStereoTrack:')

def launchExport():
    
    # Set Export Format
    do_command('SetPreference: Name="FileFormats/MP3RateModeChoice" Value="CBR" Reload=1')
    do_command('SetPreference: Name="FileFormats/MP3Bitrate" Value="128" Reload=1')
    
    statusLabel.config(text="Working.",fg='#4b6efa')
     
    exportPath = os.path.join(entryExportPath.get(), '')
    copyPath = os.path.join(entryCopyPath.get(), '')
    
    print("exportPath: " + exportPath)
    print("copyPath: " + copyPath)
    
    if not path.exists(exportPath):
        expErrorMsg = "Export Path " + exportPath + " is not found. \n Export Aborted."
        messagebox.showwarning(title="Warning", message=expErrorMsg)
        root.destroy()
        
    if not path.exists(copyPath):
        copyErrorMsg = "Copy Path " + copyPath + " is not found. \n Export Aborted."
        messagebox.showwarning(title="Warning", message=copyErrorMsg)
        root.destroy()
        
        # TODO only test copypath if copy is on

    # Export Lama/Chi
    if export_radio.get() == 1:
        top_track_output = exportPath + datetime.today().strftime('%y%m%d') + '-DKR-' + year + '-' + session + '-Lama.mp3'
        bottom_track_output = exportPath + datetime.today().strftime('%y%m%d') + '-DKR-' + year + '-' + session + '-Chi.mp3'

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
            shutil.copy(top_track_output, copyPath)
        # If copy Chi
        if copy_chi.get() == 1 :
            shutil.copy(bottom_track_output, copyPath)
        
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

    root.destroy()

# Functions - End 
  
# Pipe Init
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
# Pipe init end
  
  
# Init session number depending on time of the day  
if datetime.today().hour < 13:
    session = "S2"
else:
    session = "S3"
    


root = Tk()
root.title('Sekhar Audacity Export')
root.geometry("500x360")

var = IntVar()

label1 = Label(root,text="Export options",font=("Arial", 16)).place(x=10,y=10)

do_command('SetPreference: Name=GUI/Theme Value=classic Reload=1')

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

labelCopyPath = Label(root,text="Export Path",font=("Arial", 13)).place(x=15,y=215)

entryCopyPath = Entry(root)
entryCopyPath.place(x=100,y=212)
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

launchButton = Button(root, text="Add Mono Track", command=addMonoTrack)
launchButton.place(x=345,y=10)

launchButton = Button(root, text="Add Stereo Track", command=addStereoTrack)
launchButton.place(x=340,y=40)

statusLabel = Label(root,text="Ready.",fg='#63c266', font=("Arial", 13))
statusLabel.place(x=130,y=305)

root.mainloop()