A CLI tool for modifying shotwell tags based on regular expression matches
against the full path of the file.

Probably only useful if you leave your photos in place, rather than letting 
Shotwell import them into a date based folder structure.

Worked for me with Shotwell 0.11 on Debian wheezy.  YMMV.

Russell Heilling <chewtoy@s8n.net>

usage: swtagger.py [-h] --pattern PATTERN [--dbdir DBDIR] [--event EVENT]
                   [tag [tag ...]]

Tag Shotwell Photos.

positional arguments:
  tag                List of tags

optional arguments:
  -h, --help         show this help message and exit
  --pattern PATTERN  a regular expression to match
  --dbdir DBDIR      Shotwell database directory
  --event EVENT      Set event name
