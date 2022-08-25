import xml.etree.ElementTree as ET
import os
import shutil

IMAGE_PATH = "JPEGImages"  # 转换yolov5前图片存放位置
ANNOTATIONS_PATH = "Annotations"  # 转换yolov5前标注文件位置

# 需要检查的类别
classes = ['wildfires', 'car', 'truck', 'excavator', 'tower_crane', 'crane']

classes_set = {"d": "tower_crane", "truckd": "truck", "struck": "truck", "wwww": "truck", "w": "truck",
               "tower_craned": "tower_crane"}  # 修改标注

dep_img = "delete/img/"
dep_xml = "delete/xml/"


# move_img 移动图片
def move_img(root, xml_filepath: str):
    img_path = root.find('path').text
    img_name = img_path.split("\\")[-1]
    shutil.move(xml_filepath, '%s%s' % (dep_xml, x))
    shutil.move('%s/%s' % (IMAGE_PATH, img_name), '%s%s' % (dep_img, img_name))


if __name__ == '__main__':
    print(os.getcwd())
    if not os.path.exists('./%s' % dep_img):
        os.makedirs('./%s' % dep_img)

    if not os.path.exists('./%s' % dep_xml):
        os.makedirs('./%s' % dep_xml)

    xml_list = os.listdir(ANNOTATIONS_PATH)
    for x in xml_list:
        xml_filepath = '%s/%s' % (ANNOTATIONS_PATH, x)
        with open(xml_filepath) as label_file:
            tree = ET.parse(label_file)
            root = tree.getroot()
            try:
                size = root.find('size')  # 图像的size
                img_w = int(size.find('width').text)  # 宽
                img_h = int(size.find('height').text)  # 高
                # 判断宽高是否为0
                if img_w == 0 or img_h == 0:
                    print("%s 图片不合格" % xml_filepath)
                    move_img(root, xml_filepath)
                    continue
            except Exception as e:
                print(str(e))
                continue

            if (len(list(root.iter('object')))) == 0:
                print("%s--无object" % xml_filepath)
                # os.rename(xml_filepath, '%s/%s' % (dep_xml, x))
                move_img(root, xml_filepath)
                continue

            for obj in root.iter('object'):  # 解析object字段
                difficult = obj.find('difficult').text
                cls = obj.find('name')
                result_cls = classes_set.get(cls.text)
                # obj.set('name', result_cls)
                if result_cls is not None:
                    cls.text = result_cls

                # if cls not in classes or int(difficult) == 2:
                # if cls.text not in classes:
                #     os.rename(xml_filepath, '%s/%s' % (dep, x))
                #     continue
            tree.write(xml_filepath)
