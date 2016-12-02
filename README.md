# Q2005a to Pidgin log converter
Converts plain text log files from Q2005a to Pidgin standard HTML format.

# Usage
./ql2pn.py [-h] --logdir LOGDIR [--resdir RESDIR]

Parameters:
 * **--logdir** or **-l** - path to Q2005a user directory;
 * **--resdir** or **-r** (optional) - path to directory for generated files;
 * **--help** or **-h** (optional) - display small help.

# Requirements
 * Python 3 (3.5 or above);
 * argparse module;
 * codecs module;
 * html module;
 * os module;
 * re module;
 * datetime module.

# License
This product is licensed under the terms of GNU General Public License version 3. You can find it here: https://www.gnu.org/licenses/gpl.html. External libraries can use another licenses, compatible with GNU GPLv3.
