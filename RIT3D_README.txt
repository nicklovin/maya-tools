"""
Hello Friends!

All you need to do is 'clone' the repositories in the links provided and move
the folders that are created by those into your
\Documents\maya\2017\scripts folder in order for maya to find them.  Do this
before you start up Maya.  Change to relevant year if not 2017.

Then write the following lines into the script editor under a Python tab, or
simply copy/paste this entire file and it'll still run properly. :)

If you run into any issues, I'm always happy to reply asap!

"""

from maya_tools import nickToolDock as tool
reload(tool)
tool.show_ui()
