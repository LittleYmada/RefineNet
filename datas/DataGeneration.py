import skimage.io as imio
import matplotlib.pyplot as plt
import os
import sys
import numpy as np

dsm_path = '/home/yamada/RefineNet/data/dsm/'
top_path = '/home/yamada/RefineNet/data/top/'
tail_len = len('.tif')
dsm_head_len = len('dsm_09cm_matching_area')
top_head_len = len('top_mosaic_09cm_area')

dsm_lists = os.listdir(dsm_path)
top_lists = os.listdir(top_path)

dsm_lists = sorted(dsm_lists, 
                   key = lambda x : int(x[dsm_head_len:-tail_len]))
top_lists = sorted(top_lists,
                   key = lambda x : int(x[top_head_len:-tail_len]))   

#calculate the number of patches to sample for an input image
def calculate_sample_num(im, height = 448, width = 448):
    return int(((im.shape[0] * im.shape[1]) / (height * width)) * 2)

#auto increment image id from 'xxx..' or xxx(int)
def id_to_int(iD):
    return int(iD)

def int_to_id(iNt, id_length):
    if iNt >= pow(10, id_length) - 1:
        assert '[Error]out of range error'
        return
    tail = str(iNt)
    iD = (id_length - len(tail)) * '0' + tail
    return iD

def increment_id(id_start = '00000', length = 5):
    if isinstance(id_start, int):
        id_length = length
        id_num_start = id_start
    else:
        id_num_start = id_to_int(id_start)
        id_length = len(id_start)
    id_num_max = pow(10,  id_length)
    
    for id_num in range(id_num_start, id_num_max):
        yield int_to_id(id_num, id_length)
        


def sample_patch(top_list, dsm_list, height = 448, width = 448):
    im_id = increment_id()
    for top_name, dsm_name in zip(top_list, dsm_list):
        print(top_name, dsm_name)
        top_impath = os.path.join(top_path, top_name)
        dsm_impath = os.path.join(dsm_path, dsm_name)
        top = imio.imread(top_impath)
        dsm = imio.imread(dsm_impath)
        num_sampled = calculate_sample_num(top, height, width)
        h_range = top.shape[0] - height
        w_range = top.shape[1] - width
        print(num_sampled)
        for i in range(num_sampled):
            h_y = np.random.randint(0, h_range)
            w_x = np.random.randint(0, w_range)
            curr_id = next(im_id)
            imio.imsave(os.path.join(gen_dsm_path, curr_id + '.tif'), dsm[h_y : h_y + height, w_x : w_x + width])
            imio.imsave(os.path.join(gen_top_path, curr_id + '.tif'), top[h_y : h_y + height, w_x : w_x + width])
         
sample_patch(top_lists, dsm_lists, height = 448, width = 448) 
