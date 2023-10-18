#!/bin/python
import os
import cli
output = cli.cli("show run")
os.chdir("/bootflash/enauto-labs/")
with open("enauto_backup/show_run.conf", "w") as f:
    f.write(output)
os.system("git add .")
os.system("git commit -am 'commited by IOS XE Automation'")
os.system("git push")
