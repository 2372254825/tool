import os
import fnmatch
import shutil


def is_file_match(filename, patterns):
    for pattern in patterns:
        print(pattern)
        if fnmatch.fnmatch(filename, pattern):
            return True
    return False


def find_special_files(root, patterns=['*'], exclude_dirs=[], exclude_patterns=[], exclude_files=['.DS_Store', 'Thumbs.db']):
    for root, dirnames, filenames in os.walk(root):
        for filename in filenames:
            print(filename)
            if filename not in exclude_files:
                if is_file_match(filename, patterns):
                    if is_file_match(filename, exclude_patterns) == False:
                        yield os.path.join(root, filename)
        for d in exclude_dirs:
            if d in dirnames:
                dirnames.remove(d)


if __name__ == '__main__':
    root_path = r"C:\Users\pjx6603\Desktop\CCzhuanche_20200611_105333 (2020-6-22 10-13-18)"
    # root_path = r"{}".format(input("txt路径: "))
    
    txt_list = list(find_special_files(root_path, patterns=['*.jpg'], exclude_dirs=[], exclude_patterns=[],exclude_files=['.DS_Store', 'Thumbs.db', '*_keyframe.txt']))
    txt_list_new_path = list(find_special_files(root_path, patterns=['*.txt'], exclude_dirs=[], exclude_patterns=[],
                                       exclude_files=['.DS_Store', 'Thumbs.db', '*_keyframe.txt']))

    for item_path in txt_list_new_path:
        # print("item_path", item_path)
        item_new_path = os.path.basename(os.path.splitext(item_path)[0])
        item_new_path_1 = os.path.split(item_path)[0]
        print('itme_1', os.path.join(item_new_path_1 + "\\" + item_new_path + ".jpg"))
        for item in txt_list:
            item_root = os.path.basename(os.path.splitext(item)[0])
            if item_new_path == item_root:
                  shutil.move(item, os.path.join(item_new_path_1 + "\\" + item_new_path + ".jpg")) 
    print("移动结束")