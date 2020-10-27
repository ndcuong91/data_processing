import hashlib
import utils
import os
import time
from datetime import datetime


def get_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def check_duplicate_files_md5(files, save_file='duplicate', delete=False, keep_1_sample_for_each_group=True ,print_process=1000):
    training_time = datetime.today().strftime('%Y-%m-%d_%H-%M')
    files_md5 = []
    is_checked = []
    is_duplicate = []
    for i in range(len(files)):
        if (i % print_process == 0):
            print('Get md5 of: ' + str(i) + " files")
        files_md5.append(get_md5(files[i]))
        is_checked.append(False)

    delete_lists=[]

    for i in range(len(files_md5)):
        if (i % print_process == 0):
            print('Check duplicated: ' + str(i) + " files")
        if (is_checked[i] == True):
            continue
        is_printed = False
        for j in range(i + 1, len(files_md5), 1):
            if (files_md5[j] == files_md5[i]):
                if (is_printed == False):
                    print('Duplicated: ' + str(i+1) + ' ' + files[i])
                    is_printed = True
                    is_duplicate.append(i)
                is_checked[j] = True
                is_duplicate.append(j)
                delete_lists.append(files[j])
                print('            ' + str(j+1) + ' ' + files[j])

        is_checked[i] = True

    list_of_duplicate_files = ''
    for i in range(len(is_duplicate)):
        list_of_duplicate_files += files[is_duplicate[i]] + '\n'

    print('Files to detele',len(delete_lists))
    if delete:
        for file in delete_lists:
            print(file)
            os.remove(file)
    utils.save_txt_file(save_file+'_'+training_time+'.txt', list_of_duplicate_files)

def test_imagededup(img_dir):  #not good for exact match
    from imagededup.methods import PHash, DHash
    phasher = PHash()

    # Generate encodings for all images in an image directory
    encodings = phasher.encode_images(image_dir=img_dir)

    # Find duplicates using the generated encodings
    duplicates = phasher.find_duplicates(encoding_map=encodings, scores=True, max_distance_threshold=0)
    #for key in duplicates:
    for key in sorted(duplicates.keys()):
        if len(duplicates[key])>0:
            print (key,':',duplicates[key])

if __name__ == '__main__':
    src_dir = '/data20.04/data/SEVT/SEVT_img_1022'
    list_files = utils.get_list_file_in_folder_and_sub_folders(src_dir)
    list_files = sorted(list_files)
    list_files = [os.path.join(src_dir, f) for f in list_files]
    check_duplicate_files_md5(list_files, delete=False, keep_1_sample_for_each_group=True)
    #test_imagededup('/data20.04/data/SEVT/SEVT_img_1022')
