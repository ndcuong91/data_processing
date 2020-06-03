import hashlib
from PIL import Image
import utils
import numpy as np
import os
import time
import imghdr


def get_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def check_duplicate_files_md5(files, save_file='duplicate.txt', delete=False, print_process=1000):
    files_md5 = []
    is_checked = []
    is_duplicate = []
    for i in range(len(files)):
        if (i % print_process == 0):
            print('Get md5 of: ' + str(i) + " files")
        files_md5.append(get_md5(files[i]))
        is_checked.append(False)

    for i in range(len(files_md5)):
        if (i % print_process == 0):
            print('Check duplicated: ' + str(i) + " files")
        if (is_checked[i] == True):
            continue
        is_printed = False
        for j in range(i + 1, len(files_md5), 1):
            if (files_md5[j] == files_md5[i]):
                if (is_printed == False):
                    print('Duplicated: ' + str(i) + ' ' + files[i])
                    is_printed = True
                    is_duplicate.append(i)

                is_checked[j] = True
                is_duplicate.append(j)
                print('            ' + str(j) + ' ' + files[j])

        is_checked[i] = True

    list_of_duplicate_files = ''
    for i in range(len(is_duplicate)):
        list_of_duplicate_files += files[is_duplicate[i]] + '\n'
        if (delete):
            os.remove(files[is_duplicate[i]])
    utils.save_txt_file(save_file, list_of_duplicate_files)

if __name__ == '__main__':
    src_dir = '/data/idcard_driverlicense/crawl_facebook/idcard_29May_refine'
    list_files = utils.get_list_file_in_folder_and_sub_folders(src_dir)
    check_duplicate_files_md5(list_files, delete=True)
