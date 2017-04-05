import numpy as np
import os
import plyvel
from PIL import Image, ImageOps
import random
import sys

#Build the database
def build_db(train_file, label_file, db_path,img_size=(224,224,3)):
    db = plyvel.DB(db_path, create_if_missing=True,, error_if_exists=True, write_buffer_size=268435456)
    wb = db.write_batch()


    img = Image.open(root+imgfile, 'r')


# Load the images from database:
def load_db():
    train_file = open()

# Write the features to database

def write_feature(key):
