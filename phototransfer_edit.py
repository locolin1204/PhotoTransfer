import os
import subprocess
from datetime import date

today = date.today()

today_month = today.strftime("%m %B")
today_year = today.strftime("%Y")

path = "/Volumes/LHTC Hard Drive 2/Photos/"
path = os.path.join(path, today_year, today_month)

subprocess.Popen(["open", path])

editing_folder = input("Drag the file here: ")
editing_folder = editing_folder.replace("\\", "")
# editing_folder = editing_folder + "\b"
editing_folder = editing_folder.rstrip()

# editing_folder = "/Volumes/LHTC Hard Drive 2/Photos/2021/08 August/27_8_2020 Clement Photoshoot"

path, export_folder = os.path.split(editing_folder)

path, month_folder = os.path.split(path)

path, year_folder = os.path.split(path)

export_path = "/Volumes/LHTC Hard Drive 2/Edited Photos/"
print("\nExport Path: ", os.path.join(export_path, year_folder, month_folder), "\n")


def check_folder(cur_path, cur_dir):
    path_created = os.path.join(cur_path, cur_dir)
    if os.path.isdir(path_created):
        print("'" + cur_dir + "'" + " exist\n")
    else:
        print("'" + cur_dir + "'" + " does not exist")
        os.chdir(export_path)
        try:
            os.mkdir(cur_dir)
        except OSError:
            print("Fail to create folder " + "'" + cur_dir + "'\n")
        else:
            print("Successfully created folder " + "'" + cur_dir + "'\n")


check_folder(export_path, year_folder)
export_path = os.path.join(export_path, year_folder)

check_folder(export_path, month_folder)
export_path = os.path.join(export_path, month_folder)

export_folder_with_edit = export_folder + " Edited"
check_folder(export_path, export_folder_with_edit)

print("Final Path: " + os.path.join(export_path, export_folder_with_edit))

subprocess.Popen(["open", export_path])
