from common import *
OUT='/workspace/tag-brand/day1/'
im=bg('bg6.jpg').convert('RGBA')
# darken left for headline
y,x=np.ogrid[:H,:W]; a=(np.clip(1-x/(W*0.62),0,1)*150).astype(np.uint8)
l=Image.new('RGBA',im.size,(0,0,0,0)); l.putalpha(Image.fromarray(np.broadcast_to(a,(H,W)).copy())); im.alpha_composite(l)
T=Image.open('thumbs6.jpg').convert('RGB'); tw=T.width//2; g=8
tiles=[T.crop((0,0,tw-g,tw-g)),T.crop((tw+g,0,T.width,tw-g)),T.crop((0,tw+g,tw-g,T.height)),T.crop((tw+g,tw+g,T.width,T.height)),
       Image.open('bg4.jpg').convert('RGB').crop((380,90,900,680))]
def thumb(src,w,h):
    s=src; r=w/h
    if s.width/s.height>r: nw=int(s.height*r); s=s.crop(((s.width-nw)//2,0,(s.width-nw)//2+nw,s.height))
    else: nh=int(s.width/r); s=s.crop((0,(s.height-nh)//2,s.width,(s.height-nh)//2+nh))
    return s.resize((w,h),Image.LANCZOS)
def rmask(w,h,r):
    m=Image.new('L',(w,h),0); ImageDraw.Draw(m).rounded_rectangle((0,0,w-1,h-1),r,fill=255); return m
# ---- phone ----
PW,PH=430,820; px,py=1070,40
sw,sh=PW-28,PH-28
screen=Image.new('RGBA',(sw,sh),(14,15,19,255)); sd=ImageDraw.Draw(screen)
# status bar placeholders
sd.ellipse((sw//2-12,14,sw//2+12,38),fill=(0,0,0))
for i in range(3): sd.rounded_rectangle((sw-80+i*18,22,sw-68+i*18,30),3,fill=(150,155,165))
# generic app header: placeholder bars, no brand
sd.rounded_rectangle((22,62,140,80),9,fill=(60,64,74)); sd.ellipse((sw-50,56,sw-22,84),fill=(40,44,54))
# Recap header
sd.ellipse((22,112,38,128),fill=ORANGE)
sd.text((48,104),'Recap',font=F(ARCH,30),fill=WHITE)
sd.rounded_rectangle((sw-118,108,sw-22,130),11,fill=(36,40,50))
# thumbnails row (5, last cut off)
TW_,TH_=80,142; tx=22; ty=150
for i,t in enumerate(tiles):
    th=thumb(t,TW_,TH_).convert('RGBA')
    ov=Image.new('RGBA',th.size,(0,0,0,0)); od=ImageDraw.Draw(ov)
    # gradient bottom
    for k in range(70): od.line((0,TH_-70+k,TW_,TH_-70+k),fill=(0,0,0,int(k*2.6)))
    cx,cy=TW_//2,TH_//2
    od.ellipse((cx-18,cy-18,cx+18,cy+18),fill=(0,0,0,140),outline=(255,255,255,230),width=3)
    od.polygon([(cx-6,cy-9),(cx-6,cy+9),(cx+10,cy)],fill=(255,255,255,240))
    od.rounded_rectangle((8,TH_-18,TW_-20,TH_-12),3,fill=(255,255,255,170))  # placeholder caption bar
    th.alpha_composite(ov)
    ring=BLUE if i%2==0 else ORANGE
    sd.rounded_rectangle((tx-4,ty-4,tx+TW_+3,ty+TH_+3),16,outline=ring+(255,),width=4)
    screen.paste(th,(tx,ty),rmask(TW_,TH_,13))
    tx+=TW_+12
# progress dots
for i in range(5): sd.ellipse((sw//2-48+i*20,ty+TH_+18,sw//2-40+i*20,ty+TH_+26),fill=ORANGE if i==0 else (70,74,84))
# feed posts (blurred)
feed=Image.new('RGBA',(sw,sh-340),(14,15,19,255)); fd=ImageDraw.Draw(feed)
yy=10
for j,src in enumerate([tiles[3],Image.open('bg3.jpg')]):
    fd.line((0,yy,sw,yy),fill=(40,44,54),width=2); yy+=16
    fd.ellipse((22,yy,64,yy+42),fill=(BLUE if j==0 else ORANGE))
    fd.rounded_rectangle((78,yy+4,220,yy+18),7,fill=(150,155,165)); fd.rounded_rectangle((78,yy+26,300,yy+38),6,fill=(90,95,105))
    yy+=56
    fd.rounded_rectangle((78,yy,sw-24,yy+12),6,fill=(120,125,135)); fd.rounded_rectangle((78,yy+20,sw-80,yy+32),6,fill=(120,125,135)); yy+=46
    ph=thumb(src.convert('RGB'),sw-102,120); feed.paste(ph,(78,yy),rmask(sw-102,120,12)); yy+=134
    for k in range(4): fd.rounded_rectangle((78+k*72,yy,118+k*72,yy+12),6,fill=(80,84,94))
    yy+=30
feed=feed.filter(ImageFilter.GaussianBlur(5))
screen.paste(feed,(0,340))
# bottom nav placeholders
sd=ImageDraw.Draw(screen)
sd.rectangle((0,sh-64,sw,sh),fill=(10,11,14))
for k in range(5): sd.rounded_rectangle((34+k*(sw-68)//4-12,sh-44,34+k*(sw-68)//4+12,sh-20),6,fill=(ORANGE if k==0 else (90,94,104)))
sd.rounded_rectangle((sw//2-70,sh-10,sw//2+70,sh-5),3,fill=(200,200,205))
# phone body
sh_l=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(sh_l).rounded_rectangle((px+14,py+24,px+PW+14,py+PH+24),56,fill=(0,0,0,210))
im.alpha_composite(sh_l.filter(ImageFilter.GaussianBlur(22)))
gl=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(gl).rounded_rectangle((px-6,py-6,px+PW+6,py+PH+6),60,outline=BLUE+(160,),width=6)
im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(14)))
d=ImageDraw.Draw(im)
d.rounded_rectangle((px,py,px+PW,py+PH),54,fill=(22,23,27),outline=(70,74,84),width=3)
d.rounded_rectangle((px+PW-1,py+180,px+PW+5,py+260),3,fill=(60,64,72))
im.paste(screen,(px+14,py+14),rmask(sw,sh,42))
# ---- headline ----
ransom(im,70,92,'RECAP',70,seed=21)
hf=F(ANTON,100); X=70; Y=210; d=ImageDraw.Draw(im)
lines=[[('The end of ',WHITE),('YOUR',YEL)],[('stream is',WHITE)],[('content too',ORANGE)]]
for ln in lines:
    cx=X
    for s,c in ln:
        shadow_text(im,(cx,Y),s,hf,fill=c); cx+=ImageDraw.Draw(im).textlength(s,font=hf)
    Y+=128
d=ImageDraw.Draw(im); d.rectangle((74,Y+24,74+300,Y+32),fill=ORANGE); d.rectangle((74+300,Y+24,74+460,Y+32),fill=BLUE)
paste_logo(im,280,(64,-56))
frame(im)
im.convert('RGB').save(OUT+'post6-twitch-recaps.png',optimize=True); print('saved')
