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


def get_files(root, name_txt):
    for item in find_special_files(root, patterns=['*.txt'], exclude_dirs=[], exclude_patterns=[],
                                       exclude_files=['.DS_Store', 'Thumbs.db', '*_keyframe.txt']):
        with open(item, 'r') as open_item:
            open_item_txt = open_item.read()
            if name_txt in open_item_txt:
                des_path = input_path + "\\"+ name_txt
                print('des_path', des_path)
                if not os.path.exists(des_path):
                    os.makedirs(des_path)
                open_item.close()
                shutil.move(item, des_path)   
            else:
                break


if __name__ == '__main__':
    # root = r'{}'.format(input('请输入文件位置:'))
    # name_txt = r"{}".format(input('属性名称:'))
    root = r"C:\Users\pjx6603\Desktop\CCzhuanche_20200611_105333 (2020-6-22 10-13-18)"
    name_txt = r"discard"
    input_path = root
    get_files(root, name_txt)




