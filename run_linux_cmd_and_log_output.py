'''
# Usage:
#     python run_and_log.py [-l <logfile>] <command> [<argument> ...]
#
# This tool will execute the specified command with the optional arguments.
# Standard output and standard error of <command> will be captured and printed
# to standard error prefixing each line with the timestamp at which the line
# was captured.
# If the -l options is used, the output will also be appended to the specified file.
# run_and_log.py will exit with the same exit code of the invoked command. If
# the specified command cannot be invoked, ./run_and_log.py will exit with
# 255.
#
# Example:
#     ./run_and_log.py -l log/output.log ls /
# Will output:
#     2017-09-21 11:00:47,569 bin
...
#     2017-09-21 11:00:47,570 vmlinuz
# and exit with 0. The output will also be store din log/output.log.
#
# Example:
#     ./run_and_log.py ls non-existing-file
# Will output:
#     2017-09-21 11:05:23,294 ls: cannot access 'non-existing-file': No such file or directory
# and exit with 2.
#
#Note: this does require that package 'moreutils' be installed on the machine
'''


import subprocess
import sys
import argparse
from datetime import datetime
from sys import stdout



#note: you need something called 'moreutils' installed for this to work
#this  prints the time stamp for non-logged files
timestamp = "| ts"

#setup the -l argument
parser = argparse.ArgumentParser()
parser.add_argument("-l", help="dump to log")
args, unknown = parser.parse_known_args()


if args.l is not None:
    try:
        #-l has apparently been called
        #grab your log file
        log = args.l
        logfile = open(log, 'a')
        #setup time stamp format
        sttime = datetime.now().strftime('%b %d %H:%M:%S - ')
        #the rest of the "arguments" are really a single command so combine them into one string
        cmdwlog = sys.argv[3:]
        str1 = ' '.join(cmdwlog)
        #run the command and print it to the screen with the timestamp
        #also log to the user's log of choice
        p = subprocess.Popen([str1], shell=True, stdout=subprocess.PIPE, stderr=stdout, executable="/bin/bash")
        for line in p.stdout:
            sys.stdout.write(sttime + line)
            logfile.write(sttime + line)
            p.wait()
    except:
        #if there is something wrong with the -l flag it will just try to do the cmd without it
        pass
else:
    #-l is not called
    #grab all of the arguments as a list then combine them into one command separated by a space
    cmd = sys.argv[1:]
    str2 = ' '.join(cmd)
    #now you have treated all 'arguments' as a single command
    #run the command and print it to the screen with the timestamp
    p1 = subprocess.Popen([str2 + timestamp], shell=True, stdout=subprocess.PIPE, stderr=stdout, executable="/bin/bash")
    print p1.communicate()[0].decode('utf-8').strip()


