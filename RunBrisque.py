import brisque as bq
from PIL import Image as imgfns
import sys
import numpy as np
import argparse
import os
import matplotlib.pyplot as plt
# Initiate the parser
parser = argparse.ArgumentParser()

# Add long and short argument
parser.add_argument("--path", "-p", help="set directory path")
parser.add_argument("--feature","-f", help="get feature vector to csv file")
parser.add_argument("--mscn","-m",help="convert img to mscn images to folder")

# Read arguments from the command line
args = parser.parse_args()
print(args)
res=[]
img=[]
# Check for --width
def openfile(filename):
    im=imgfns.open(filename)
    im=np.array(im)
    return(im)
#@openfile

if args.mscn:
    os.mkdir(args.mscn)
          


if args.path:
    #=len(os.listdir(args.path))
    for filename in os.listdir(args.path):
        #print(args.path+filename)
        im=openfile(args.path+filename)
        res.append(bq.brisque(im))
        im_mscn=bq.calculate_mscn(im)
        mscn_min=np.min(im_mscn)
        mscn_max=np.max(im_mscn)
        im_mscn=(im_mscn-mscn_min)/(mscn_max-mscn_min) #to make the values between 0 to 1
        filename=filename.split('.')[0]

        if args.mscn:
            plt.imsave(f'{args.mscn}/{filename}_mscn.jpg', im_mscn, cmap='Greys')
          

else:  
    filename=sys.argv[0]
    im=openfile(args.path+filename)
    res.append(bq.brisque(im))
    im_mscn=bq.calculate_mscn(im)
import pandas as pd
#res=np.concatenate(res)
res=np.vstack(res)
res=pd.DataFrame(res)


Param_type=['shape','mean','lvar','rvar']
Orient_s=['V','H','D1','D2'] #vertical, horizontal, main diagonal, off diagonal
colnames = ['shape_GDD','var_GDD']+[f'{param}_{pw_p}' for param in Param_type for pw_p in Orient_s]
colnames_all =[f'{resol}_{names}' for resol in ['orig','low'] for names in colnames]
res.columns=colnames_all
filenames=os.listdir(args.path)
res['filenames']=filenames
print(res)
if args.feature:
    res.to_csv(args.feature+'.csv')




#print(img)

