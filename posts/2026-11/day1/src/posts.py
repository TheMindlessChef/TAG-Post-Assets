from common import *
import math, sys
OUT='/workspace/tag-brand/day1/'
def save(im,name): im.convert('RGB').save(OUT+name,optimize=True); print('saved',name)

# ---------- POST 1 ----------
def p1():
    im=bg('bg1.jpg').convert('RGBA')
    # darken top-left for text
    g=np.zeros((H,W),np.uint8); y,x=np.ogrid[:H,:W]
    a=np.clip(1-(x/W*1.3+y/H*1.6)/1.6,0,1)*200; g=Image.fromarray(a.astype(np.uint8))
    sh=Image.new('RGBA',im.size,(0,0,0,0)); sh.putalpha(g); im.alpha_composite(sh)
    ransom(im,60,50,'10 NOV',104,seed=3)
    ransom(im,60,175,'PRE-LOAD',104,seed=7)
    d=ImageDraw.Draw(im)
    f=F(ANTON,78); x=64; y=320
    shadow_text(im,(x,y),'Sort ',f)
    w1=d.textlength('Sort ',font=f)
    shadow_text(im,(x+w1,y),'YOUR',f,fill=YEL)
    w2=d.textlength('YOUR ',font=f)
    shadow_text(im,(x+w1+w2,y),'audio first',f)
    d.rectangle((66,420,66+380,428),fill=ORANGE); d.rectangle((66+380,420,66+560,428),fill=BLUE)
    paste_logo(im,300,(-48,-40),plate=True)
    frame(im); save(im,'post1-gta-preload-audio.png')

# ---------- POST 2 ----------
def p2():
    im=Image.new('RGBA',(W,H),(10,12,18,255))
    # subtle radial lift
    y,x=np.ogrid[:H,:W]; r=np.sqrt(((x-W*0.5)/W)**2+((y-H*0.6)/H)**2)
    a=(np.clip(0.6-r,0,1)*90).astype(np.uint8); l=Image.new('RGBA',im.size,(20,40,80,0)); l.putalpha(Image.fromarray(a)); im.alpha_composite(l)
    d=ImageDraw.Draw(im)
    X0,X1,Y0,Y1=120,1480,330,780; mid=(Y0+Y1)//2
    for i in range(0,13):
        xx=X0+i*(X1-X0)/12; d.line((xx,Y0,xx,Y1),fill=(40,48,64),width=1)
    for j in range(0,7):
        yy=Y0+j*(Y1-Y0)/6; d.line((X0,yy,X1,yy),fill=(40,48,64),width=1)
    d.line((X0,mid,X1,mid),fill=(80,90,110),width=2)
    t=np.linspace(0,1,600)
    cut=-70/(1+np.exp((t-0.17)/0.045))      # gentle low shelf cut
    bump=55*np.exp(-((t-0.66)/0.075)**2)     # small upper-mid lift
    yv=mid-(cut+bump); xv=X0+t*(X1-X0)
    pts=list(zip(xv,yv))
    # fill under curve
    fl=Image.new('RGBA',im.size,(0,0,0,0)); fd=ImageDraw.Draw(fl)
    fd.polygon(pts+[(X1,mid),(X0,mid)],fill=(30,123,255,40)); im.alpha_composite(fl)
    # gradient coloured curve: blue -> orange
    def dc(dd,wid):
        for i in range(len(pts)-1):
            k=t[i]; c=tuple(int(BLUE[j]*(1-k)+ORANGE[j]*k) for j in range(3))
            dd.line((pts[i],pts[i+1]),fill=c+(255,),width=wid)
    glow(im,lambda dd:dc(dd,7),radius=16,strength=3)
    d=ImageDraw.Draw(im)
    # labels
    lf=F(ANTON,52)
    i_low=int(0.08*600); xl,yl=pts[i_low]
    d.line((xl,yl+12,xl+40,yl+120),fill=BLUE,width=4); d.ellipse((xl-9,yl-9,xl+9,yl+9),fill=BLUE)
    shadow_text(im,(xl+46,yl+108),'trim lows',lf,fill=(120,175,255))
    i_up=int(0.66*600); xu,yu=pts[i_up]
    d=ImageDraw.Draw(im); d.ellipse((xu-10,yu-10,xu+10,yu+10),fill=ORANGE)
    d.line((xu,yu-14,xu,yu-58),fill=ORANGE,width=4)
    shadow_text(im,(xu,yu-64),'lift upper mids',lf,fill=ORANGE,anchor='md')
    af=F(BEBAS,40)
    for s,k in (('LOWS',0.06),('MIDS',0.42),('HIGHS',0.92)):
        d.text((X0+k*(X1-X0),Y1+20),s,font=af,fill=(130,140,160),anchor='ma')
    # headline
    shadow_text(im,(80,52),'Footsteps buried?',F(ANTON,104))
    hf=F(ANTON,64); shadow_text(im,(84,182),'Small moves beat ',hf,fill=WHITE)
    ww=ImageDraw.Draw(im).textlength('Small moves beat ',font=hf)
    shadow_text(im,(84+ww,182),'big ones.',hf,fill=ORANGE)
    paste_logo(im,280,(-60,48),shadow=True)
    frame(im); save(im,'post2-footsteps-eq.png')

# ---------- POST 3 ----------
def p3():
    im=bg('bg3.jpg').convert('RGBA')
    ov=Image.new('RGBA',im.size,(0,0,0,70)); im.alpha_composite(ov)
    cx0,cy0,cx1,cy1=610,90,1530,810
    sh=Image.new('RGBA',im.size,(0,0,0,0)); sd=ImageDraw.Draw(sh)
    sd.rounded_rectangle((cx0+10,cy0+16,cx1+10,cy1+16),34,fill=(0,0,0,200)); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
    card=Image.new('RGBA',im.size,(0,0,0,0)); cd=ImageDraw.Draw(card)
    cd.rounded_rectangle((cx0,cy0,cx1,cy1),34,fill=(14,16,22,235),outline=BLUE,width=5)
    im.alpha_composite(card)
    d=ImageDraw.Draw(im)
    lx,ly,lw,lh=paste_logo(im,250,(cx0+50,cy0+42),shadow=False)
    d.text((cx1-50,cy0+70),'CHECKLIST',font=F(BEBAS,46),fill=ORANGE,anchor='ra')
    hf=F(ANTON,70); y=cy0+215
    d.text((cx0+50,y),'Before ',font=hf,fill=WHITE); w=d.textlength('Before ',font=hf)
    d.text((cx0+50+w,y),'YOU',font=hf,fill=YEL); w+=d.textlength('YOU ',font=hf)
    d.text((cx0+50+w,y),'update OBS 33',font=hf,fill=WHITE)
    d.line((cx0+50,y+112,cx1-50,y+112),fill=(60,70,90),width=3)
    items=[('1','Export Profile +','Scene Collection',BLUE),('2','Safe Mode if it','misbehaves',ORANGE)]
    iy=y+150
    bf=F(ARCH,44)
    for n,a,b,c in items:
        d.rounded_rectangle((cx0+50,iy,cx0+140,iy+90),16,fill=c)
        d.text((cx0+95,iy+45),n,font=F(ANTON,62),fill=WHITE,anchor='mm')
        # tick box
        d.rounded_rectangle((cx1-120,iy+12,cx1-54,iy+78),10,outline=(200,200,210),width=4)
        d.text((cx0+170,iy-4),a,font=bf,fill=WHITE); d.text((cx0+170,iy+50),b,font=bf,fill=WHITE)
        iy+=150
    frame(im); save(im,'post3-obs33-checklist.png')

# ---------- POST 4 ----------
def p4():
    im=bg('bg4.jpg').convert('RGBA')
    d=ImageDraw.Draw(im)
    # looping sound: left bedroom area ; one-off: bottom-right room
    LX,LY=600,440; OX,OY=1000,600
    def loop_draw(dd):
        for r in (30,52,74):
            dd.ellipse((LX-r,LY-r,LX+r,LY+r),outline=BLUE+(255,),width=5)
        dd.ellipse((LX-16,LY-16,LX+16,LY+16),fill=BLUE+(255,))
    glow(im,loop_draw,radius=14,strength=3)
    # loop arrow
    d=ImageDraw.Draw(im)
    d.arc((LX-100,LY-100,LX+100,LY+100),200,500,fill=(150,200,255),width=5)
    ang=math.radians(500-360); ax,ay=LX+100*math.cos(ang),LY+100*math.sin(ang)
    d.polygon([(ax-14,ay-10),(ax+12,ay-14),(ax+2,ay+14)],fill=(150,200,255))
    # one-off ping, fading
    l=Image.new('RGBA',im.size,(0,0,0,0)); ld=ImageDraw.Draw(l)
    for i,r in enumerate((26,52,80,110,142)):
        a=int(255*(1-i/5)**1.6)
        ld.ellipse((OX-r,OY-r,OX+r,OY+r),outline=ORANGE+(a,),width=max(2,6-i))
    ld.ellipse((OX-13,OY-13,OX+13,OY+13),fill=ORANGE+(255,))
    g=l.filter(ImageFilter.GaussianBlur(12)); im.alpha_composite(g); im.alpha_composite(g); im.alpha_composite(l)
    # ghostly wisp glow
    gl=Image.new('RGBA',im.size,(0,0,0,0)); gd=ImageDraw.Draw(gl)
    gd.ellipse((780,250,980,420),fill=(150,255,230,40)); im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(50)))
    # labels
    lf=F(ANTON,50); sf=F(BEBAS,40)
    d=ImageDraw.Draw(im)
    pass
    shadow_text(im,(476,LY-62),'looping:',lf,fill=(120,175,255),anchor='ra')
    shadow_text(im,(476,LY+2),'stays on screen',lf,anchor='ra')
    d=ImageDraw.Draw(im)
    shadow_text(im,(1176,OY-62),'one-off:',lf,fill=ORANGE)
    shadow_text(im,(1176,OY+2),'pings and fades',lf)
    # headline
    shadow_text(im,(60,40),'Sound is gameplay info',F(ANTON,84))
    ransom(im,62,150,'RESONANCE',62,seed=11)
    paste_logo(im,280,(-50,-44),plate=True)
    frame(im); save(im,'post4-phasmo-resonance-radar.png')

# ---------- POST 5 ----------
def p5():
    im=bg('bg5.jpg').convert('RGBA')
    d=ImageDraw.Draw(im)
    LY=712  # path at Haggis' feet
    # travelled path behind him (dashed, dim)
    for x in range(60,640,34): d.line((x,LY,x+18,LY),fill=(90,100,120),width=6)
    def strip(dd):
        dd.line((640,LY,1540,LY),fill=BLUE+(255,),width=8)
    glow(im,strip,radius=10,strength=2)
    d=ImageDraw.Draw(im)
    nodes=[(1010,'A4G closed','launch',True),(1240,'MultiChat',None,False),(1460,'Studio','Apps',False)]
    lf=F(ANTON,42)
    for x,a,b,nxt in nodes:
        if nxt:
            def nd(dd,x=x): dd.ellipse((x-30,LY-30,x+30,LY+30),fill=ORANGE+(255,))
            glow(im,nd,radius=18,strength=3); d=ImageDraw.Draw(im)
            d.polygon([(x-10,LY-14),(x-10,LY+14),(x+14,LY)],fill=WHITE)
            # NEXT tag
            ransom(im,x-78,LY-150,'NEXT',52,seed=4,palette=[(ORANGE,WHITE),(WHITE,BLACK),(YEL,BLACK),(RED,WHITE)])
            col=ORANGE
        else:
            d.ellipse((x-20,LY-20,x+20,LY+20),fill=(18,22,30),outline=BLUE,width=6); col=WHITE
        d=ImageDraw.Draw(im)
        shadow_text(im,(x,LY+42),a,lf,fill=col,anchor='ma')
        if b: shadow_text(im,(x,LY+90),b,lf,fill=col,anchor='ma')
        d=ImageDraw.Draw(im)
    d.polygon([(1540,LY-16),(1540,LY+16),(1568,LY)],fill=BLUE)
    paste_logo(im,290,(44,40),plate=False)
    # header top-right
    shadow_text(im,(1550,46),'Build-in-public',F(ANTON,92),anchor='ra')
    ransom_w=ransom_width('CHECK-IN',66,seed=9)
    ransom(im,1550-ransom_w,170,'CHECK-IN',66,seed=9)
    frame(im); save(im,'post5-build-in-public-roadmap.png')

for n in sys.argv[1:]: globals()['p'+n]()
