import os
import cv2
import shutil
import fnmatch
import numpy as np
from PIL import Image
from numpy import average, dot, linalg



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



# 对图片进行统一化处理
def get_thum(image, size = (64,64), greyscale = False):
    image = image.resize(size, Image.ANTIALIAS)                    # 利用image对图像大小重新设置, Image.ANTIALIAS为高质量的 
    if greyscale:
        image = image.convert('L')                                 # 将图片转换为L模式，其为灰度图，其每个像素用8个bit表示 
    return image



def img_similarity_vectors_via_numpy(image1,image2):                # 计算图片之间的余弦距离
    
    image1 = get_thum(image1)
    image2 = get_thum(image2)
    images = [image1,image2]
    vectors = []
    norms = []
    for image in images:
        vector = []
        for pixel_turple in image.getdata():
            vector.append(average(pixel_turple))
        vectors.append(vector)                                              
        norms.append(linalg.norm(vector, 2))           # linalg=linear（线性）+algebra（代数），norm则表示范数                                                   
    a, b = vectors                                     # 求图片的范数                     
    a_norm, b_norm = norms
    res = dot(a / a_norm, b / b_norm)                   # dot返回的是点积，对二维数组（矩阵）进行计算
    return res


def img_cropImg(find_special_files):
    itme_list = list(find_special_files(root, patterns=["*jpg"],exclude_dirs=['001,002'], exclude_patterns=[], exclude_files=['.DS_Store','Thumbs.db']))
    txt_list = list(find_special_files(root, patterns=["*.txt"],exclude_dirs=[], exclude_patterns=[], exclude_files=['.DS_Store','Thumbs.db']))
    

    xlist = itme_list
    # print(xlist)
    ylist = itme_list
    np_list = []
    index = 0
    index_ln = 0
    for item in itme_list:                                                              #通过遍历获取全部的jpg
        for txt in txt_list:
            with open(txt, 'r' ,encoding='utf-8') as f:
                content = f.readlines()
                content_dict = eval(content[0])
                # print('content',type(content_dict),content_dict['rect'])
                rect = content_dict['rect'].split(',')
                # print('rect', rect)
                rect_x_min = rect[0]
                rect_y_min = rect[3]
                rect_x_max = rect[1]
                rect_y_max = rect[2]
                                                                                        
                img = cv2.imread(item)                                                   #opencv打开遍历的图片
                cropImg = img[int(rect_x_min):int(rect_y_min),int(rect_x_max):int(rect_y_max)]                                   #截取指定区域图片的坐标，此时cropImg对象是一个numpy数组
                np_list.append(cropImg)

        index +=1
        index_ln +=1
        print('index-1',index-1)
        print('index_ln',index_ln-2) 
        # if not os.path.exists(os.path.join(root+"\\"+"002")):         #在原路径下创建001文件夹用于存放按照区域坐标截取的图片
        #         os.makedirs(os.path.join(root+"\\"+"002"))
        # cv2.imwrite(os.path.join(root+"\\"+"002"+"\\"+os.path.basename(item)), np_list[index_ln-2])     #保存图片                  
        # print('np_list[i]',index-1,np_list[index+1])
        # print('np_list[i_count]', np_list[index_ln])
        # print(np_list[i])
        image1 = Image.fromarray(np_list[index_ln-2])                              #Image.fromarray() 可以读取以数组方式储存的图片
        image2 = Image.fromarray(np_list[index-1])
        cosine = img_similarity_vectors_via_numpy(image1,image2)                   #cosine:   两张图片的余弦相似度
        print("余弦相似度为 ：", cosine)
        if cosine < 0.99: 
            print(item)                                                        #判断余弦相似度如果<=0.97
            if not os.path.exists(os.path.join(root+"\\"+"001")):                  #创建002文件夹用于存放相似度较底的图片 
                os.makedirs(os.path.join(root+"\\"+"001"))
            shutil.copy(item,os.path.join(root+"\\"+"001"))                    #把相似度较低的图片移动到刚创建的文件夹          
                                                                                                
                        
       

if __name__ == "__main__":
    root = r"D:\555\002\vdo_0000000006_0000000008"
    find_special_files(root)
    img_cropImg(find_special_files)
   
    