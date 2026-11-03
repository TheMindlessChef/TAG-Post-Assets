from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import numpy as np, random
G='/usr/share/fonts/truetype/sand-box/google/'
ANTON=G+'Anton/Anton-Regular.ttf'; ARCH=G+'Archivo Black/ArchivoBlack-Regular.ttf'; BEBAS=G+'Bebas Neue/BebasNeue-Regular.ttf'
SERIF='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
BLUE=(30,123,255); ORANGE=(255,122,26); RED=(220,30,40); YEL=(250,210,20); WHITE=(245,245,245); BLACK=(12,12,12)
W,H=1600,900
def F(p,s): return ImageFont.truetype(p,s)
def bg(path):
    im=Image.open(path).convert('RGB')
    return im.resize((W,H),Image.LANCZOS)
def logo(width):
    a=Image.open('/workspace/tag-brand/avatar.jpg').convert('RGB')
    arr=np.asarray(a).astype(float)
    lum=arr.max(axis=2)
    ys,xs=np.where(lum>40)
    x0,x1,y0,y1=xs.min()-6,xs.max()+6,ys.min()-6,ys.max()+6
    a=a.crop((x0,y0,x1,y1))
    h=round(a.height*width/a.width)
    a=a.resize((width,h),Image.LANCZOS)
    arr=np.asarray(a).astype(float)
    m=arr.max(axis=2)
    alpha=np.clip((m-18)/(90-18),0,1)  # black -> transparent, metal -> opaque
    rgb=np.clip(arr/np.maximum(alpha[...,None],1e-3)*(alpha[...,None]>0),0,255)
    rgb=np.where(alpha[...,None]>0, np.minimum(rgb,255), 0)
    out=np.dstack([rgb, alpha*255]).astype(np.uint8)
    return Image.fromarray(out,'RGBA').filter(ImageFilter.UnsharpMask(1.2,80,2))
def paste_logo(im,width,pos,shadow=True,plate=False):
    L=logo(width); x,y=pos
    if x<0: x=W-L.width+x
    if y<0: y=H-L.height+y
    if plate:
        pl=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(pl)
        d.rounded_rectangle((x-18,y-14,x+L.width+18,y+L.height+14),18,fill=(0,0,0,170))
        im.alpha_composite(pl.filter(ImageFilter.GaussianBlur(6)))
    if shadow:
        s=Image.new('RGBA',im.size,(0,0,0,0)); a=L.split()[3]
        sh=Image.new('RGBA',L.size,(0,0,0,255)); sh.putalpha(a)
        s.paste(sh,(x+4,y+5),sh); im.alpha_composite(s.filter(ImageFilter.GaussianBlur(5)))
    im.alpha_composite(L,(x,y)); return (x,y,L.width,L.height)
def text(d,xy,s,font,fill=WHITE,stroke=0,sfill=BLACK,anchor='la'):
    d.text(xy,s,font=font,fill=fill,stroke_width=stroke,stroke_fill=sfill,anchor=anchor)
def shadow_text(im,xy,s,font,fill=WHITE,anchor='la',blur=8,off=(3,4)):
    l=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(l)
    d.text((xy[0]+off[0],xy[1]+off[1]),s,font=font,fill=(0,0,0,230),anchor=anchor)
    im.alpha_composite(l.filter(ImageFilter.GaussianBlur(blur)))
    ImageDraw.Draw(im).text(xy,s,font=font,fill=fill,anchor=anchor)
def ransom(im,x,y,word,size,seed=1,gap=4,palette=None):
    """cut-out letter blocks echoing the banner; returns end x"""
    rnd=random.Random(seed)
    pal=palette or [(WHITE,BLACK),(BLACK,WHITE),(RED,WHITE),(YEL,BLACK),(WHITE,RED),(BLACK,YEL)]
    fonts=[ARCH,ANTON,SERIF,BEBAS]
    cx=x
    for i,ch in enumerate(word):
        if ch==' ': cx+=int(size*0.35); continue
        bgc,fg=pal[rnd.randrange(len(pal))]
        fp=fonts[rnd.randrange(len(fonts))]; fs=int(size*(0.82 if fp in(ARCH,SERIF) else 1.0)*rnd.uniform(0.92,1.06))
        f=F(fp,fs); bb=f.getbbox(ch)
        tw,th=bb[2]-bb[0],bb[3]-bb[1]
        pad=int(size*0.13); bw,bh=tw+2*pad,int(size*1.08)
        t=Image.new('RGBA',(bw,bh),bgc+(255,)); td=ImageDraw.Draw(t)
        td.text((bw/2,bh/2),ch,font=f,fill=fg,anchor='mm')
        t=t.rotate(rnd.uniform(-6,6),resample=Image.BICUBIC,expand=True)
        sh=Image.new('RGBA',t.size,(0,0,0,0)); sh.paste((0,0,0,180),(0,0),t.split()[3])
        oy=int(rnd.uniform(-0.06,0.06)*size)
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)),(cx+4,y+oy+6))
        im.alpha_composite(t,(cx,y+oy)); cx+=t.width+gap
    return cx
def ransom_width(word,size,seed=1,gap=4):
    tmp=Image.new('RGBA',(4000,400)); return ransom(tmp,0,50,word,size,seed,gap)
def glow(im,draw_fn,radius=14,strength=2):
    l=Image.new('RGBA',im.size,(0,0,0,0)); draw_fn(ImageDraw.Draw(l))
    g=l.filter(ImageFilter.GaussianBlur(radius))
    for _ in range(strength): im.alpha_composite(g)
    im.alpha_composite(l)
def vignette(im,amt=0.55):
    y,x=np.ogrid[:H,:W]; r=np.sqrt(((x-W/2)/(W/2))**2+((y-H/2)/(H/2))**2)
    a=(np.clip(r-0.55,0,1)*amt*255).astype(np.uint8)
    v=Image.new('RGBA',im.size,(0,0,0,0)); v.putalpha(Image.fromarray(a)); im.alpha_composite(v)
def frame(im,c=BLUE,w=10):
    ImageDraw.Draw(im).rectangle((0,0,W-1,H-1),outline=c,width=w)
