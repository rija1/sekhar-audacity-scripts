#!/bin/bash
pyinstaller --specpath bin/mac/spec --distpath bin/mac/dist --workpath bin/mac/build --noconsole --onedir --hidden-import="appscript" sekhar_audacity_export.py