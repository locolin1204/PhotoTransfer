import os
import subprocess
from datetime import date

og_path = "/Volumes/LHTC Hard Drive 2/Film/"

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

event = input("\nWhat is this film (Format: brand_filmNameWithISO | fuji_fujicolor100) : ")
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

def open_file(path):
    subprocess.Popen(["open", path])

TO = TOpath + "/" + dirname

open_file("/Users/colinlo/Downloads")
open_file(TO)