#!/bin/python
import os
import cli
output = cli.cli("show run")
os.chdir("enauto_backup/")
with open("show_run.conf", "w") as f:
    f.write(output)
os.system("git add .")
os.system("git commit -am 'commited by IOS XE Automation'")
