# Build a transparent TAG wordmark from avatar.jpg using a luminance mask.
from PIL import Image
import numpy as np
im = np.asarray(Image.open('/workspace/tag-brand/avatar.jpg').convert('RGB')).astype(float)/255
L = 0.2126*im[...,0]+0.7152*im[...,1]+0.0722*im[...,2]
lo, hi = 0.10, 0.55          # below lo = background, above hi = fully opaque
a = np.clip((L-lo)/(hi-lo), 0, 1)
ys, xs = np.where(a > 0.05)
pad = 4
y0, y1, x0, x1 = ys.min()-pad, ys.max()+pad, xs.min()-pad, xs.max()+pad
# un-premultiply against black so edges aren't muddy, keep chrome tones
rgb = np.clip(im/np.maximum(a[...,None],1e-3)*np.minimum(a[...,None]*4,1)+0*im, 0, 1)
rgb = np.where(a[...,None]>0.02, np.clip(im/np.maximum(a[...,None],0.35),0,1), 0)
out = np.dstack([rgb, a])[y0:y1, x0:x1]
Image.fromarray((out*255).astype('uint8'), 'RGBA').save('logo.png')
print(out.shape)
