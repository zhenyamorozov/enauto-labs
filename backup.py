#!/bin/python
"""This Guest Shell script backs up, commits and pushes running config.
EEM configuration to automatically trigger the script:
event manager applet GUESTSHELL-CONFIG-CHANGE-TO-GIT
 event syslog pattern "%SYS-5-CONFIG_I: Configured from"
 action 0.0 cli command "enable"
 action 1.0 cli command "guestshell run python /bootflash/enauto-labs/backup.py"
"""
import os
import cli
output = cli.cli("show run")
os.chdir("/bootflash/enauto-labs/")
with open("enauto_backup/show_run.conf", "w") as f:
    f.write(output)
print("Saved configuration file locally")
os.system("git add .")
os.system("git commit -am 'commited by IOS XE Automation'")
os.system("git push")
print("Pushed changes to remote repository")
