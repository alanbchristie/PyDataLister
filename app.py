#!/usr/bin/env python3

# A simple utility that list files in a directory before pausing,
# optionally doing some CPU-intensive work and leaving.
# This super-simple piece of code is used to illustrate the mounting
# of volumes in an OpenShift cluster and its reaction to a heavily-loaded
# process (Pod).
#
# The images waits for PRE_LIST_SLEEP_S seconds prior to listing the data
# directory pausing and looking busy before finally leaving.
#
# This image can be configured (via environment variables):
#
# - DATA_PATH                   # Path to the data directory
# - PRE_LIST_SLEEP              # Seconds to sleep before listing the directory
# - POST_LIST_SLEEP             # Seconds to sleep after listing the directory
# - POST_SLEEP_BUSY_PERIOD      # Number of seconds to look 'busy'
# - POST_SLEEP_BUSY_WORK        # The number of factorials to run
# - BUSY_PROCESSES              # Number of busy processes to run
# - USE_MEMORY_M                # Amount of memory to consume (approx)
#
# Alan Christie
# 3 January 2018

import datetime
import math
from multiprocessing import Process
import os
import sys
import time

# Take the data path from the environment or use a default.
DATA_PATH = os.environ.get('DATA_PATH', '/source')
# Same with the rest
PRE_LIST_SLEEP_S = float(os.environ.get('PRE_LIST_SLEEP', '20.0'))
POST_LIST_SLEEP_S = float(os.environ.get('POST_LIST_SLEEP', '300.0'))
POST_SLEEP_BUSY_PERIOD_S = float(os.environ.get('POST_SLEEP_BUSY_PERIOD', '0.0'))
POST_SLEEP_BUSY_WORK = int(os.environ.get('POST_SLEEP_BUSY_WORK', '0'))
BUSY_PROCESSES = int(os.environ.get('BUSY_PROCESSES', '1'))
USE_MEMORY_M = int(os.environ.get('USE_MEMORY_M', '0'))

# Memory is allocated prior to the POST_LIST_SLEEP period.

# The complexity of the problem ... a large factorial.
# This factorial takes about 8 seconds on a 2.7GHz i7
# MacBook Pro (15-inch, 2016)
FACTORIAL = 1000000


def thread_function(duration_s=0, work=0):
    """Tries to burn up the CPU for the prescribed duration (controlled by
    POST_SLEEP_BUSY_PERIOD_S) or number of iterations (controlled by
    POST_SLEEP_BUSY_WORK).

    :param duration_s: The duration of time to run. Either this is set or
                       work is set. If both are set duration_s is used.
    :param work: The amount of work (number of factorials to run). Either this
                 is set or the duration is set. If both are set duration_s is
                 used.
    """
    if duration_s > 0:
        duration_t = datetime.timedelta(seconds=duration_s)
        start_time = datetime.datetime.now()
    iterations = 0

    done = False
    factorials = []
    while not done:
        factorials.append(math.factorial(FACTORIAL))
        # Again?
        if duration_s > 0:
            elapsed = datetime.datetime.now() - start_time
            if elapsed >= duration_t:
                done = True
        else:
            iterations += 1
            if iterations >= work:
                done = True
    return factorials


# -----------------------------------------------------------------------------

# Echo configuration...
print("---")
print("DATA_PATH = %s" % DATA_PATH)
print("PRE_LIST_SLEEP_S = %sS" % PRE_LIST_SLEEP_S)
print("POST_LIST_SLEEP_S = %sS" % POST_LIST_SLEEP_S)
print("POST_SLEEP_BUSY_PERIOD_S = %sS" % POST_SLEEP_BUSY_PERIOD_S)
print("POST_SLEEP_BUSY_WORK = %s" % POST_SLEEP_BUSY_WORK)
print("BUSY_PROCESSES = %s" % BUSY_PROCESSES)
print("USE_MEMORY_M = %sMB" % USE_MEMORY_M)
print("---")
sys.stdout.flush()

# Sleep for a while before listing...
print("Resting before looking (%sS)..." % PRE_LIST_SLEEP_S)
sys.stdout.flush()
time.sleep(PRE_LIST_SLEEP_S)
print("Hello!")
print("---")

# Echo what was found...
if os.path.exists(DATA_PATH):
    print( "Data directory (%s) exists and contains..." % DATA_PATH)
    file_names = os.listdir(DATA_PATH)
    if file_names:
        for file_name in file_names:
            print( os.path.join(DATA_PATH, file_name))
    else:
        print("...Nothing!")
else:
    print("Ooops .. the data directory does not exist! (%s)" % DATA_PATH)

memory = []
if USE_MEMORY_M:
    print("---")
    print("Allocating memory (%sMB)..." % USE_MEMORY_M)
    for meg in range(USE_MEMORY_M):
        memory.append([0] * 1048576)

# Sleep for a while before th optional busy cycle...
print("---")
print("Resting before busy (%sS)..." % POST_LIST_SLEEP_S)
sys.stdout.flush()
time.sleep(POST_LIST_SLEEP_S)

if (POST_SLEEP_BUSY_PERIOD_S <= 0.0 and POST_SLEEP_BUSY_WORK <= 0) \
        or BUSY_PROCESSES <= 0:
    print("---")
    print("Told not to look busy.")
else:
    print("---")
    if POST_SLEEP_BUSY_PERIOD_S:
        print("Trying to look busy (PERIOD=%sS)..." % POST_SLEEP_BUSY_PERIOD_S)
    else:
        print("Trying to look busy (WORK=%s)..." % POST_SLEEP_BUSY_WORK)
    processes = []
    for i in range(1, BUSY_PROCESSES + 1):
        print("+ Process %d..." % i)
        sys.stdout.flush()
        p = Process(target=thread_function,
                    args=(POST_SLEEP_BUSY_PERIOD_S, POST_SLEEP_BUSY_WORK))
        p.start()
        processes.append(p)
    print("Waiting for processes...")
    waiting_for = BUSY_PROCESSES
    for p in processes:
        p.join()
        waiting_for -= 1
        print("- %d..." % waiting_for)
        sys.stdout.flush()

print("---")
print("Bye")
print("---")
