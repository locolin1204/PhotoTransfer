import os
from datetime import date
import shutil
import math
import subprocess
import time
import asyncio
from asyncio.subprocess import PIPE, Process
import glob


def create_folders(path_test, path_create, cur_date):
    if os.path.isdir(path_test):
        print("Folder " + "'" + cur_date + "'" + " exists")
    else:
        print("Folder " + "'" + cur_date + "'" + " does not exist")
        os.chdir(path_create)
        try:
            os.mkdir(cur_date)
        except OSError:
            print("Fail to create folder " + "'" + cur_date + "'\n")
        else:
            print("Successfully created folder " + "'" + cur_date + "'\n")


def create_event_folder(today_dir_name):
    print("Status:", end=" ")
    try:
        os.mkdir(today_dir_name)
    except OSError:
        print("Fail to create folder " + "'" + today_dir_name + "'")
    else:
        print("Successfully created folder " + "'" + today_dir_name + "'")


def open_file(path):
    subprocess.Popen(["open", path])


def count_files_and_check_arw(path, list_ext):
    total_files = 0
    is_arw = False
    for root, subdirs, files in os.walk(path):
        for file in files:
            pure_filename, ext = os.path.splitext(file)
            if ext[1:].lower() in list_ext and pure_filename[:2] != "._":
                total_files += 1
                if ext[1:].lower() == 'arw' and is_arw is False:
                    is_arw = True
    return total_files, is_arw


def copy_files(source_path, dest_path, total_files, list_ext):
    copied_files = 0
    print("Copied 0%. Copied 0 files", end="\r")
    for root, subdirs, files in os.walk(source_path):
        for file in files:
            transfer_path = os.path.join(root, file)
            pure_filename, ext = os.path.splitext(file)
            if ext[1:].lower() in list_ext and pure_filename[:2] != "._":
                try:
                    shutil.move(transfer_path, dest_path)  # copy or move
                    copied_files += 1
                    print("Copied {}%. Copied {} files".format(math.floor(copied_files / total_files * 100),
                                                               copied_files), end="\r")
                except OSError:
                    print("Fail to Copy")

    print("\nStatus: Copied all files\n")
    return copied_files


def remove_files_by_extension(root_dir, extension):
    files_removed = 0
    print("Remove: ", root_dir)

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            pure_filename, ext = os.path.splitext(file)
            if file.lower().endswith(extension) and pure_filename[:2] != "._":
                file_path = os.path.join(root, file)
                try:
                    # print("remove:", file_path)
                    os.remove(file_path)  # remove the file
                    files_removed += 1
                except Exception as e:
                    print(f"Failed to remove {file_path}: {e}")

    print(f"Total files removed ({extension.upper()}): {files_removed}")


async def monitor_directory(dest, total_files):
    initial_files = set(os.listdir(dest))
    converted_count = 0

    print("Converted 0%. Converted 0 files", end="\r")
    while True:
        await asyncio.sleep(0.1)  # poll every 0.1 second
        current_files = set(os.listdir(dest))
        if len(current_files) > len(initial_files):
            new_files = current_files - initial_files
            for file in new_files:
                converted_count += 1
                print("Converted {}%. Converted {} files".format(math.floor(converted_count / total_files * 100), converted_count), end="\r")
            initial_files = current_files
        if converted_count == total_files:
            return converted_count


async def run_command(command):
    process = await asyncio.create_subprocess_exec(*command, stdout=PIPE, stderr=PIPE)

    # wait for the subprocess to finish
    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        print("\n\nStatus: Conversion Successful")
    else:
        print(f"Error: {stderr.decode()}")


async def batch_convert(dng_converter_path, dest_dir, source_pattern):
    # find all files matching the source pattern
    source_files = glob.glob(source_pattern, recursive=True)

    command = [dng_converter_path, "-d", dest_dir, "-p1", "-cr14.0", "-fl", "-mp"] + source_files

    await run_command(command)


async def dng_convert(dng_converter_path, dest_dir, source_pattern, total_files):
    result = await asyncio.gather(
        monitor_directory(dest_dir, total_files),
        batch_convert(dng_converter_path, dest_dir, source_pattern)
    )
    convert_extension(dest_dir, '.dng', '.DNG')

    return result[0]


def convert_extension(directory, old_ext, new_ext):
    for filename in os.listdir(directory):
        # check if the current file ends with the old extension
        if filename.lower().endswith(old_ext):
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, filename[:-len(old_ext)] + new_ext)
            # rename the file
            os.rename(old_file, new_file)


def check_file_exists(directory, extensions):
    for filename in os.listdir(directory):
        if any(filename.lower().endswith(ext) for ext in extensions):
            return True
    return False


def main():
    original_photo_dest = "/Volumes/LHTC Hard Drive 2/Photos/"
    # original_photo_dest = "/Users/colinlo/Downloads/Photos/DEST/"
    original_video_dest = "/Volumes/LHTC Hard Drive 2/Videos/"
    # original_video_dest = "/Users/colinlo/Downloads/Photos/VID/"

    source_path = '/Volumes/NO NAME/DCIM'
    source_path_vid = '/Volumes/NO NAME/PRIVATE/M4ROOT/CLIP'

    img_ext = ['jpg', 'png', 'nef', 'arw', 'cr2']
    vid_ext = ['mov', 'mp4']

    today = date.today()
    this_year = today.strftime("%Y")
    this_month = today.strftime("%m %B")

    # path for testing if directory of particular year/month exist
    path_test_year = original_photo_dest + this_year
    path_test_month = original_photo_dest + this_year + "/" + this_month

    print()

    # create folders for year and month
    create_folders(path_test_year, original_photo_dest, this_year)
    create_folders(path_test_month, path_test_year, this_month)

    # change directory to the month directory
    month_path = path_test_month
    os.chdir(month_path)
    print("Path:", month_path)

    # ask for today's event
    event = input("\nWhat is today's event: ")
    today_date = today.strftime("%Y-%m-%d")
    today_dir_name = today_date + " " + event
    print("Directory:", today_dir_name)

    # create directory for today's event
    create_event_folder(today_dir_name)

    # photo destination path
    dest_path = month_path + "/" + today_dir_name

    # count and print total files
    total_files, is_arw = count_files_and_check_arw(source_path, img_ext)
    print("\nTotal files:", total_files)

    # check if video exist
    is_video_exist = check_file_exists(source_path_vid, vid_ext)

    if is_arw:
        print("Found ARW. Perform Conversion to DNG.")

        start_time = time.time()

        dng_converter_path = "/Applications/Adobe DNG Converter.app/Contents/MacOS/Adobe DNG Converter"

        loop = asyncio.get_event_loop()
        success_copied_files = loop.run_until_complete(dng_convert(
            dng_converter_path,
            dest_path,
            source_path + "/*MSDCF/*.ARW",
            total_files
        ))
        loop.close()

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Total elapsed time: {elapsed_time:.2f}s \n")

        print("Status: Converted all files\n")

        # transfer video if exists
        if is_video_exist:
            print("\nVideo Exist.\n")

            # create folder for year
            create_folders(original_video_dest + this_year, original_video_dest, this_year)

            # change directory to year
            os.chdir(original_video_dest + this_year)
            print("Path:", original_video_dest + this_year)

            # create directory for today's event
            create_event_folder(today_dir_name)

            # count total video files
            total_video_files, _ = count_files_and_check_arw(source_path_vid, vid_ext)
            print("\nTotal video files:", total_video_files)

            # video destination path
            vid_dest_path = original_video_dest + this_year + "/" + today_dir_name

            success_copied_video_files = copy_files(source_path_vid, vid_dest_path, total_video_files, vid_ext)

            open_file(vid_dest_path)
            open_file(source_path_vid)

    else:
        success_copied_files = copy_files(source_path, dest_path, total_files, img_ext)

    print("Summary:")
    print(f"Total Photos (Transferred): {total_files}({success_copied_files})")
    if is_video_exist:
        print(f"Total Videos (Transferred): {total_video_files}({success_copied_video_files})")

    for root, subdirs, files in os.walk("/Volumes/NO NAME/DCIM"):
        for subdir in subdirs:
            open_file("/Volumes/NO NAME/DCIM/" + subdir)

    open_file(dest_path)

    # confirmation for deletion
    is_delete = input("\nDelete Files? (y/n): ")

    if is_delete != "n":
        remove_files_by_extension(source_path, "arw")
        remove_files_by_extension(source_path_vid, "xml")
        remove_files_by_extension("/Volumes/NO NAME/PRIVATE/M4ROOT/THMBNL", "jpg")


if __name__ == "__main__":
    main()
