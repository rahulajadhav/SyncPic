import shutil, os , time
from pathlib import Path
from PIL import Image
import datetime
import cv2
import numpy as np
import re

count = 0
srcefiles = []
duplicatefiles= []
sourceinput = input("Please enter source drive (example D:/) : ")
sourcepath = sourceinput.split()
typeinput = input("Please enter file extension example .jpg or .doc : ")
type=typeinput.split()

for p in sourcepath :
# r=root, d=directories, f = files
    for r, d, f in os.walk(p):
        for file in f:
            for extension in type :
                if extension.casefold() in file.casefold():
                    srcefiles.append(os.path.join(r, file))

for p in sourcepath :
# r=root, d=directories, f = files
    for r, d, f in os.walk(p):
        for file in f:
            for extension in type :
                if extension.casefold() in file.casefold():
                    duplicatefiles.append(os.path.join(r, file))

        
def checkTakendateExist(srcimage,destimage):
    try :
        im = Image.open(srcimage)
        exif = im.getexif()
        creation_time_src = exif.get(36867)
        im.close()
        try :
            im = Image.open(destimage)
            exif = im.getexif()
            creation_time_dest = exif.get(36867)
            im.close()
            if creation_time_src == creation_time_dest and creation_time_src!=None and creation_time_dest!=None and creation_time!="0000:00:00 00:00:00":
                code = 0
                return code
            else:
                code = 4
                return code
        except :
            code = 1
            return code
    except:
        try :
            im = Image.open(destimage)
            exif = im.getexif()
            creation_time_src = exif.get(36867)
            im.close()
            code = 2
            return code
        except:
            code = 3
            return code
            

        
def operation(f,d):
    f=f.replace("\\", "/")
    d=d.replace("\\", "/")
    original = cv2.imread(f)
    duplicate = cv2.imread(d)
    #cv2.imshow("Original", original)
    #cv2.imshow("Duplicate", duplicate)
    #cv2.waitKey(0)
    if original.shape == duplicate.shape:
        difference = cv2.subtract(original, duplicate)
        b, g, r = cv2.split(difference)
        if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
            code = checkTakendateExist(f,d)
            if code == 0 :
                os.remove(d)
                print("File already exists deleting extra file ")
            if code == 1 :
                print("Taken code exists in source, deleting destination file : ")
                os.remove(f)
            if code == 2 :
                os.remove(f)
            if code == 3 :
                print("Taken code doest not exists in destination or source : ")
                os.remove(d)
            if code == 4 :
                src_size = os.stat(f).st_size
                dest_size = os.stat(d).st_size
                if src_size >= dest_size :
                    os.remove(d)
                    print("src file size > so deleted backup and added src file")
                else:
                    os.remove(f)
                    print("dest file size > so deleted src file")
for f in srcefiles: 
    for d in duplicatefiles :
        if f!=d:
            operation(f,d)
        else :
            print("No files")