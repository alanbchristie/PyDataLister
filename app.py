#!/usr/bin/env python

# A simple utility that list files in a directory before pausing and leaving.
# This super-simple piece of code is used to illustrate the mounting
# of volumes in an OpenShift cluster.
#
# Alan Christie
# 17 October 2017

import os
import time

# Take the data path from the environment or use a default.
DATA_PATH = os.environ.get('DATA_PATH', '/data')
# Before and after listing the directory content
# the application pauses briefly...
PRE_LIST_SLEEP_S = 2.0
POST_LIST_SLEEP_S = 8.0

# Sleep for a while before listing
print "Resting before looking (%sS)..." % PRE_LIST_SLEEP_S
time.sleep(PRE_LIST_SLEEP_S)
print "Hello!"
print "---"

if os.path.exists(DATA_PATH):
    file_names = os.listdir(DATA_PATH)
    for file_name in file_names:
        print os.path.join(DATA_PATH, file_name)
else:
    print "Ooops .. the data directory does not exist! (%s)" % DATA_PATH

# Sleep for a while before leaving
print "---"
print "Resting before exit (%sS)..." % POST_LIST_SLEEP_S
time.sleep(POST_LIST_SLEEP_S)
print "Bye!"
