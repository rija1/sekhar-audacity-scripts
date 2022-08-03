#!/bin/bash
pyinstaller --specpath bin/mac/spec --distpath bin/mac/dist --workpath bin/mac/build --noconsole --onefile --hidden-import="appscript" audacity_export.py