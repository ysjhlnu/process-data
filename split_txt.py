# 划分数据集

import os
import shutil
import random

train_val_percent = 0.1
train_percent = 0.9
BASE_DIR = "base"  # 基础目录
xml_path = 'Annotations'  # 标注文件
txt_save_path = 'ImageSets'  # 划分后的标注文件保存位置

base_txt_save_path = '%s/%s/' % (BASE_DIR, txt_save_path)

total_xml = os.listdir(xml_path)
num = len(total_xml)
xml_list = range(num)
tv = int(num * train_val_percent)  # 校验集数量
tr = int(tv * train_percent)  # 测试集数量
random_train_val = random.sample(xml_list, tv)  # 从所有list中返回tv个数量的项目
train_test = random.sample(random_train_val, tr)  # 测试

print("total xml num: %d, train: %d, train test: %d, train val: %d\n" % (num, num - tv, tr, tv))

if not os.path.exists(base_txt_save_path):
    os.makedirs(base_txt_save_path)
else:
    shutil.rmtree(base_txt_save_path)
    os.makedirs(base_txt_save_path)

ftrainval = open('%s/trainval.txt' % base_txt_save_path, 'w')
ftest = open('%s/test.txt' % base_txt_save_path, 'w')  # 测试
ftrain = open('%s/train.txt' % base_txt_save_path, 'w')  # 训练集
fval = open('%s/val.txt' % base_txt_save_path, 'w')  #
for i in xml_list:
    name = total_xml[i][:-4] + '\n'
    if i in random_train_val:
        ftrainval.write(name)
        if i in train_test:
            ftest.write(name)
        else:
            fval.write(name)
    else:
        ftrain.write(name)
ftrainval.close()
ftrain.close()
fval.close()
ftest.close()
