import os
import numpy as np
import cv2

def get_combine():
    output_dir='/home/ubuntu/flaskapp/uploads/c'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    input_dir='/home/ubuntu/flaskapp/uploads/b'
    b_dir='/home/ubuntu/flaskapp/uploads/a'
    H=256
    skipped = 0
    for f in os.listdir(input_dir):
        src_path=os.path.join(input_dir,f)
        img1=cv2.imread(src_path)
        flag=0
        sibling_path = os.path.join(b_dir, f)
        if os.path.exists(sibling_path):
            img2 = cv2.imread(sibling_path)
            flag=1
            print(flag)
        if(flag==0):
            continue
        img1=cv2.resize(img1, (H,H)) 
        img2=cv2.resize(img2, (H,H)) 
        vis = np.zeros((H, 2*H,3), np.uint8)
        vis[:H, :H] = img1
        vis[:H, H:2*H] = img2
        ff=f.split('.')
        dst_path = os.path.join(output_dir, ff[0] + ".png")
        cv2.imwrite(dst_path,vis)

            # complete()
get_combine()