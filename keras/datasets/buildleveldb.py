import numpy as np
import os
import plyvel as ply
from PIL import *
import random
import sys
import StringIO

#Build the database
#Build the database
def build_db(rootpath,train_file, db_path,img_size=(224,224)):
    db = ply.DB(db_path, create_if_missing=True, write_buffer_size=268435456)
    wb = db.write_batch()

    count = 0

    with open(train_file) as f:
        for fileName in f.read().splitlines():
            print fileName
            img = Image.open(rootpath+fileName, 'r')
            img.thumbnail(img_size, Image.ANTIALIAS)
            img = ImageOps.fit(img,img_size,Image.ANTIALIAS)
            wb.put('%08d_%s' % (count, fileName), img.tobytes())
            count = count + 1
            if count % 1000 == 0:
                wb.write()
                del wb
                wb = db.write_batch()
                print 'Processed %i images.' % count

    if count % 1000 == 0:
        wb.write()
        print "Processed a total of %i images." %count
    else:
        print "Processed a total of %i images." %count



# Load the images from database:
def load_db(db_path, img_size=(224,224)):
    db = ply.DB(db_path, create_if_missing=True)
    imglist = []
    for key, value in db():
        imgitem = db.get(key)
        img = Image.frombytes('RGB',img_size,imgtest)
        imglist.append(img)

    return imglist

# Write the features to database

def write_feature(db_path, converted_db_path, method='isohashlp', count,
                      vector_size = 64, iter = 200):

#write hash features as key to index the images
