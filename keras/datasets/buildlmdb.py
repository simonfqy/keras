import numpy as np
import os
import lmdb
from PIL import Image, ImageOps
import random
import sys

# Load the dataset to database, build the leveldb
# from the dataset:
# input: train.txt Path to the images
#
def build_db(db_path, rootpath, trainfile, imgsize=(224,224)):

    env = lmdb.open(dbpath, map_size=2684354560)

    with env.begin(write=True) as tdb:
        with open(train_file) as f:
            for fileName in f.read().splitlines():
                print fileName
                img = Image.open(rootpath+fileName, 'r')
                img.thumbnail(img_size, Image.ANTIALIAS)
                img = ImageOps.fit(img,img_size,Image.ANTIALIAS)
                str_id = '{:08}'.format(i)
                tdb.put(str_id.encode('ascii'), img.tobytes())





def load_db(db_path):

# Write the deep convolutional features of images
# to database

def write_feature():

# Write the deep convolutional features of images
# to database
