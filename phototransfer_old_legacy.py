import os
from datetime import date

og_path = "/Volumes/LHTC Hard Drive 2/Photos/"

today = date.today()
pathyear = today.strftime("%Y")
pathmonth = today.strftime("%m %B")

path_test_year = og_path + pathyear
path_test_month = og_path + pathyear + "/" + pathmonth

print("")

def create_folders(path_test, path_create, cur_date):
    if os.path.isdir(path_test):
        print("Folder " + "'" + cur_date + "'" + " exits")
    else:
        print("Folder " + "'" + cur_date + "'" + " does not exit")
        os.chdir(path_create)
        try:
            os.mkdir(cur_date)
        except OSError:
            print("Fail to create folder " + "'" + cur_date + "'\n")
        else:
            print("Successfully created folder " + "'" + cur_date + "'\n")


create_folders(path_test_year, og_path, pathyear)
create_folders(path_test_month, path_test_year, pathmonth)

TOpath = path_test_month
os.chdir(TOpath)
print("\nPath:", TOpath)

event = input("\nWhat is today's event: ")
todayfile = today.strftime("%Y-%m-%d")
dirname = todayfile + " " + event
print("Directory:", dirname)

print("Status:", end=" ")
try:
    os.mkdir(todayfile + " " + event)
except OSError:
    print("Fail to create folder " + "'" + dirname + "'")
else:
    print("Successfully created folder " + "'" + dirname + "'")

import shutil

TO = TOpath + "/" + dirname

FROM = '/Volumes/NO NAME'

imgext = ['jpg', 'png', 'nef', 'arw', 'cr2']

i = 0
total = 0

for root, subdirs, files in os.walk(FROM):
    for file in files:
        transferpath = os.path.join(root, file)
        purefile, ext = os.path.splitext(file)
        for loop in imgext:
            if loop == ext[1:].lower():
                total += 1
print("\nTotal files:", total)

import math
for root, subdirs, files in os.walk(FROM):
    for file in files:
        transferpath = os.path.join(root, file)
        purefile, ext = os.path.splitext(file)
        for loop in imgext:
            if loop == ext[1:].lower():
                try:
                    shutil.move(transferpath, TO) #copy or move
                    i += 1
                    print("Copied {}%. Copied {} files".format(math.floor(i / total * 100), i), end="\r")
                except OSError:
                    print("Fail to Copy")
        # if total == i:
        #     print("Copied {}%. Copied {} files".format(math.floor(i / total * 100), i))


print("\nStatus: Copied all files\n")

import subprocess

def open_file(path):
    subprocess.Popen(["open", path])

for root, subdirs, files in os.walk("/Volumes/NO NAME/DCIM"):
    for subdir in subdirs:
        open_file("/Volumes/NO NAME/DCIM/" + subdir)

open_file(TO)

