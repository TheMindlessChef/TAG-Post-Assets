import cv2, numpy as np
im=cv2.imread('bg5-original.jpg').astype(np.float32)
H,W=im.shape[:2]
def feather(mask,r): return cv2.GaussianBlur(mask.astype(np.float32),(0,0),r)
def clone(img,box,dy,dx,r=3):
    x0,y0,x1,y1=box; m=np.zeros((H,W),np.float32); m[y0:y1,x0:x1]=1; m=feather(m,r)[...,None]
    src=np.roll(img,(-dy,-dx),axis=(0,1))  # pixel at p takes from p+(dy,dx)
    return img*(1-m)+src*m
b,g,r=[im[...,i] for i in range(3)]
# 1) shoulder X patch: replace with jacket fabric cloned from just below
out=clone(im,(534,237,568,265),28,0,r=2.5)
# 2) shorts lettering: gold/orange pixels in the shorts region
mask=np.zeros((H,W),np.uint8)
reg=(slice(372,440),slice(575,630))
gold=((r>g*0.9)&(r>b*1.25)&(r>90)).astype(np.uint8)
sub=np.zeros((H,W),np.uint8); sub[reg]=gold[reg]
mask=cv2.dilate(sub,np.ones((5,5),np.uint8),iterations=1)
out8=np.clip(out,0,255).astype(np.uint8)
inp=cv2.inpaint(out8,mask*255,4,cv2.INPAINT_TELEA).astype(np.float32)
# add denim-like grain back into the inpainted area
rng=np.random.default_rng(3); noise=rng.normal(0,6,(H,W,1)).astype(np.float32)
mf=feather(mask,1.2)[...,None]
out=inp+noise*mf
cv2.imwrite('bg5.jpg',np.clip(out,0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,97])
cv2.imwrite('/tmp/mask5.png',mask*255)
print(mask.sum())
