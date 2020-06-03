import os


def open_txt_file(file_path, content, encoding='utf-8'):
    with open(file_path, 'rb', encoding=encoding) as file:
        file.write(content)

def save_txt_file(file_path, content, encoding='utf-8'):
    with open(file_path, 'w', encoding=encoding) as file:
        file.write(content)

def rename_files(dir):
    list_file = get_list_file_in_folder(dir)
    count=1
    for file in list_file:
        print(file)
        extension = os.path.splitext(file)[1]
        new_name =str(count).zfill(5)+extension
        os.rename(os.path.join(dir, file), os.path.join(dir, new_name))
        count+=1


def get_list_file_in_folder_and_sub_folders(dir, ext=['jpg', 'png', 'JPG', 'PNG']):
    all_files = []
    for path, subdirs, files in os.walk(dir):
        for name in files:
            extension = os.path.splitext(name)[1].replace('.','')
            if extension in ext:
                all_files.append(os.path.join(path, name).replace(dir+'/',''))
    return all_files


def get_list_file_in_folder(dir, ext=['jpg', 'png', 'JPG', 'PNG']):
    included_extensions = ext
    file_names = [fn for fn in os.listdir(dir)
                  if any(fn.endswith(ext) for ext in included_extensions)]
    return file_names


def get_list_dir_in_folder(dir):
    sub_dir = [o for o in os.listdir(dir) if os.path.isdir(os.path.join(dir, o))]
    return sub_dir

if __name__ == '__main__':
    src_dir='/data/idcard_driverlicense/crawl_facebook/idcard_1June/merge'
    rename_files(src_dir)