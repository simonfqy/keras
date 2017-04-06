import numpy as np
import os
import plyvel as ply
from PIL import *
import random
import sys
import StringIO
import leargist as lgist
from sklearn.decomposition import PCA

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
    return count



# Load the images from database:
def load_db(db_path):

# Write the features to database

# Returns the eigenvectors of X.
def eigs_descend(X):
    eig_vals, eig_vecs = np.linalg.eig(X)
    # To get descending order, negate and sort in ascending order.
    sequence = np.argsort(-eig_vals)
    return eig_vecs[:, sequence]

def isoHash_lp(Lambda, iter, vector_size):
    a = np.trace(Lambda)/vector_size
    # Getting random orthogonal matrix U.
    R = np.random.random((vector_size, vector_size))
    U, _, _ = np.linalg.svd(R, compute_uv=1)
    Z = (U.dot(Lambda)).dot(U.T)

    for i in range(iter):
        # find T
        T = Z
        for j in range(vector_size):
            T[j, j] = a
        # find Z
        Q = eigs_descend(T)
        Z = (Q.dot(Lambda)).dot(Q.T)
    Q = Q.T
    return Q

# write hash features as key to index the images
def write_feature(db_path, converted_db_path, method='isohashlp', count,
    vector_size = 64, iter = 200):
    # A very primitive implementation. Need to refactor the code if 
    # want to make it more versatile to a diversity of methods.
    if method.lower() == 'isohashlp':
        db = ply.DB(db_path)
        # I think we cannot modify in place. Have to create a new database.
        converted_db = ply.DB(converted_db_path, create_if_missing=True,
         write_buffer_size=268435456)
        # Assume we directly use the dimension 960 of gist. Can modify it later
        gist_dim = 960
        gists = np.zeros((gist_dim, count))
        i = 0
        with converted_db.write_batch() as converted_wb:
            for key, value in db:                
                img = Image.frombytes('RGB', (224, 224), value)
                gist = lgist.color_gist(img)
                # The 960-dimensional gists, serving as inputs for isoHash.
                # TODO: could have better implementation
                gists[:, i] = gist
                i += 1
            # zero center the data
            avg = np.sum(gists, axis=1)/count
            avg = avg.reshape((gist_dim, 1))
            gists = gists - avg

            # This PCA method is said to be inefficient. Can switch.
            pca = PCA(n_components = vector_size)
            gist_reduced = (pca.fit_transform(gists.T)).T
            # Each row is a Principal Component.
            # gist_reduced is W^T*X
            Lambda = np.dot(gist_reduced, gist_reduced.T)          

            Q = isoHash_lp(Lambda, iter, vector_size)
            # TODO: Use sign function to get Y.
            Y = (Q.T).dot(gist_reduced)
            Y = (Y >= 0)*1

            for i in range(count):
                converted_key = Y[:, i].tobytes()
                converted_wb.put(converted_key, value)
                # Note that if want to reconstruct from string, must use
                # np.fromstring(converted_key, dtype = int)

