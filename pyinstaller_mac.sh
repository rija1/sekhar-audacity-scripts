#!/bin/bash
pyinstaller --icon=sekhar_audacity.icns --specpath bin/mac/spec --distpath bin/mac/dist --workpath bin/mac/build --noconsole --onedir --hidden-import="appscript" sekhar_audacity_export.py