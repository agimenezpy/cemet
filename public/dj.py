#!/usr/bin/python
import sys, os

# Add a custom Python path.
sys.path.insert(0, "/home/agimenez/Desktop/Politecnica/cemetwiki/cemet/")

# Switch to the directory of your project. (Optional.)
#os.chdir("/media/KINGSTON/Facultad/")

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")


