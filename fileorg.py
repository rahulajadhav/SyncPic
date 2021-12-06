import shutil, os , time
from pathlib import Path
from PIL import Image
import datetime
import cv2
import numpy as np
import re

count = 0
copied = 0
files = []
sourceinput = input("Please enter source drive (example D:/) : ")
sourcepath = sourceinput.split()
destination = input("Enter Destination for backup : ")
destinationskip=os.path.split(destination)
typeinput = input("Please enter file extension example .jpg or .doc : ")
type=typeinput.split()
choice=input("Do you want to copy or move Data . enter 1 for move enter 0 for copy : ")

for p in sourcepath :
# r=root, d=directories, f = files
    for r, d, f in os.walk(p):
        exclude = set([destinationskip[1]])#[destinationskip[1]]
        d[:] = [dir for dir in d if dir not in exclude]
        for file in f:
            for extension in type :
                if extension.casefold() in file.casefold():
                    files.append(os.path.join(r, file))


def checkdirectory(destination,year, month):
    global path
    path = destination+"/"+year+"/"+month
    if os.path.exists(path):
        print("Folder Exists")
        return True
    else:
        os.makedirs(path)
        print("Folder created")
        return True
        
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
            

        
def operation(path,filename,choice,f):
    exists= path+"/"+filename
    f=f.replace("\\", "/")
    print(f)
    print(exists)
    if f!=exists :
        if choice=="1" :     
            if os.path.isfile(exists):
                    try:
                        original = cv2.imread(f)
                        duplicate = cv2.imread(exists)
                        #cv2.imshow("Original", original)
                        #cv2.imshow("Duplicate", duplicate)
                        #cv2.waitKey(0)
                        if original.shape == duplicate.shape:
                            difference = cv2.subtract(original, duplicate)
                            b, g, r = cv2.split(difference)
                            if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                                code = checkTakendateExist(f,exists)
                                if code == 0 :
                                    print("Taken code exists in both deleting source file : ")
                                    os.remove(f)
                                if code == 1 :
                                    print("Taken code exists in source, deleting destination file : ")
                                    os.remove(exists)
                                    shutil.move(f, path)
                                if code == 2 :
                                    print("Taken code exists in destination, deleting source file : ")
                                    os.remove(f)
                                if code == 3 :
                                    print("Taken code doest not exists in destination or source : ")
                                if code == 4 :
                                    src_size = os.stat(f).st_size
                                    dest_size = os.stat(exists).st_size
                                    if src_size > dest_size :
                                        os.remove(exists)
                                        shutil.move(f, path)
                                        print("src file size > so deleted backup and added src file")
                                    else:
                                        os.remove(f)
                                        print("dest file size > so deleted src file")
                            else:
                                basefilenameList=filename.split('.')
                                basefilename=basefilenameList[0]
                                basefilenameext=basefilenameList[1]
                                c = 1
                                copy=0
                                while c != 0 :
                                    newfilename= path+"/"+filename
                                    if os.path.isfile(newfilename):               
                                        filename=basefilename+"(copy-"+str(copy)+")."+basefilenameext
                                        copy+=1
                                    else:
                                        c=0
                                shutil.move(f, path+"/"+filename)
                                print(f +" File moved to " +path)
                        else:
                            basefilenameList=filename.split('.')
                            basefilename=basefilenameList[0]
                            basefilename=basefilenameList[0]
                            basefilenameext=basefilenameList[1]
                            c = 1
                            copy=0
                            while c != 0 :
                                newfilename= path+"/"+filename
                                if os.path.isfile(newfilename):               
                                    filename=basefilename+"(copy-"+str(copy)+")."+basefilenameext
                                    copy+=1
                                else:
                                    c=0
                            shutil.move(f, path+"/"+filename)
                            print(f +" File moved to " +path)
                    except :
                        print(f + " file not moved because of src folder name  :")
                        exit()
            else :
                shutil.move(f, path)
                print(f +" File moved to " +path)
        if choice=="0" :
            if os.path.isfile(exists):
                    try:
                        original = cv2.imread(f)
                        duplicate = cv2.imread(exists)
                        #cv2.imshow("Original", original)
                        #cv2.imshow("Duplicate", duplicate)
                        #cv2.waitKey(0)
                        if original.shape == duplicate.shape:
                            difference = cv2.subtract(original, duplicate)
                            b, g, r = cv2.split(difference)
                            if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                                code = checkTakendateExist(f,exists)
                                if code == 0 :
                                    print("File Already exists , skipped copy : ")
                                if code == 1 :
                                    print("File in source code is original , deleting destination and replacing file : ")
                                    os.remove(exists)
                                    shutil.copy(f, path)
                                if code == 2 :
                                    print("File Already exists , skipped copy : ")
                                if code == 3 :
                                    print("File Already exists , skipped copy : ")
                                if code == 4 :
                                    src_size = os.stat(f).st_size
                                    dest_size = os.stat(exists).st_size
                                    if src_size > dest_size :
                                        print("src file is greater in size , so deleted backup and added src file")
                                        os.remove(exists)
                                        shutil.copy(f, path)
                                    else:
                                        print("File Already exists , skipped copy : ")
                            else:
                                basefilenameList=filename.split('.')
                                basefilename=basefilenameList[0]
                                basefilenameext=basefilenameList[1]
                                c = 1
                                copy=0
                                while c != 0 :
                                    newfilename= path+"/"+filename
                                    if os.path.isfile(newfilename):               
                                        filename=basefilename+"(copy-"+str(copy)+")."+basefilenameext
                                        copy+=1
                                    else:
                                        c=0
                                shutil.move(f, path+"/"+filename)
                                print(f +" File moved to " +path)
                        else:
                            basefilenameList=filename.split('.')
                            basefilename=basefilenameList[0]
                            basefilename=basefilenameList[0]
                            basefilenameext=basefilenameList[1]
                            c = 1
                            copy=0
                            while c != 0 :
                                newfilename= path+"/"+filename
                                if os.path.isfile(newfilename):               
                                    filename=basefilename+"(copy-"+str(copy)+")."+basefilenameext
                                    copy+=1
                                else:
                                    c=0
                            shutil.copy(f, path+"/"+filename)
                            print(f +" File copied to " +path)

                    except :
                        print(f + " file not moved because of src folder name  :")
                        exit()
            else :
                shutil.copy(f, path)
                print(f +" File copied to " +path)
    else :
        print("Dest and src same : ")
for f in files:   
    try :
        print(f)
        filename =os.path.basename(f)
        im = Image.open(f)
        exif = im.getexif()
        creation_time = exif.get(36867)
        im.close()
        if creation_time is not None :
            ttime = creation_time[:10]
            needTime = ttime.replace(" ", "0")
        if creation_time is not None and needTime != "0000:00:00" and needTime != '':
            x = datetime.datetime.strptime(needTime, "%Y:%m:%d").date()
            year = x.year
            month_number = datetime.date(2015, x.month, 1).strftime('%m')
            month_name = datetime.date(2015, x.month, 1).strftime('%B')
            month=month_number+"-"+month_name
            checkDirectoryStatus = checkdirectory(destination,str(year), str(month))
            if checkDirectoryStatus== True :
                im.close()
                operation(path,filename,choice,f)
            else:
                print("Error in file creation please try again")
        else:
            
            filename =os.path.basename(f)
            basefilenameList=filename.split('.')
            basefilename=basefilenameList[0]
            phoneRegex = re.compile(r'((_|-)20\d{6}(_|-)|(20\d{2}-\d{2}-\d{2}))')
            mo1 = phoneRegex.search(basefilename)
            try :
                if mo1 != None:
                    print(mo1.group())
                    x = datetime.datetime.strptime(mo1.group(), "%Y%m%d").date()
                    year = x.year
                    month_number = datetime.date(2015, x.month, 1).strftime('%m')
                    month_name = datetime.date(2015, x.month, 1).strftime('%B')
                    month=month_number+"-"+month_name
                    checkDirectoryStatus = checkdirectory(destination,str(year), str(month))
                    if checkDirectoryStatus== True :
                        operation(path,filename,choice,f)
                    else:
                        print("Error in file creation please try again")
                else :
                    print("images without taken date and without name in date : ")
                '''
                    getmyear = time.strftime('%Y', time.localtime(os.path.getmtime(f)))
                    getmmonth = time.strftime('%m''-''%B', time.localtime(os.path.getmtime(f)))
                    checkDirectoryStatus = checkdirectory(destination,str(getmyear),str(getmmonth))
                    if checkDirectoryStatus== True :
                        operation(path,filename,choice,f)
                    else:
                        print("Error in file creation please try again")'''
            except:
                    print("images without taken date and without name in date : ")                
                    '''
                    getmyear = time.strftime('%Y', time.localtime(os.path.getmtime(f)))
                    getmmonth = time.strftime('%m''-''%B', time.localtime(os.path.getmtime(f)))
                    checkDirectoryStatus = checkdirectory(destination,str(getmyear),str(getmmonth))
                    if checkDirectoryStatus== True :
                        operation(path,filename,choice,f)
                    else:
                        print("Error in file creation please try again")'''
    except:
        print("Image file corrupted : ")