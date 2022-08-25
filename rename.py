# -*- coding: utf-8 -*- 

import os
import sys



j = 40000


src_dir = sys.argv[1]

for files in os.listdir(src_dir):
    img_filename = src_dir + '/' + files
    print(img_filename)
    if img_filename.find('异物') >= 0:
        destfilename = src_dir + '/' + 'foreign_body' + '.' + str(j) + '.jpg'
        os.rename(img_filename, destfilename)
        j = j+1
        print(destfilename)
    
