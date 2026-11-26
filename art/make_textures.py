
import colorsys, math, random, os
from PIL import Image, ImageDraw, ImageFont

def hx(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def ramp(base, n=5, spread=0.10):
    r,g,b=[c/255 for c in hx(base)]; h,l,s=colorsys.rgb_to_hls(r,g,b); out=[]
    for i in range(n):
        k=(i-2)
        hh=(h + (-0.025*k if k<0 else -0.012*k)) % 1.0   # shadows cooler, lights warmer
        if k<0: hh=(h+0.02*(-k))%1.0
        ll=min(0.95,max(0.05,l+spread*k)); ss=min(1,max(0,s*(1-0.08*abs(k))))
        out.append(tuple(int(c*255) for c in colorsys.hls_to_rgb(hh,ll,ss))+(255,))
    return out  # 0 darkest .. 4 lightest

class Px:
    def __init__(s): s.p={}
    def set(s,x,y,c):
        if 0<=x<16 and 0<=y<16: s.p[(x,y)]=c
    def get(s,x,y): return s.p.get((x,y))
    def outline(s, k=0.55):
        keys=list(s.p)
        edge=[(x,y) for (x,y) in keys if any((x+dx,y+dy) not in s.p for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))]
        for (x,y) in edge:
            r,g,b,a=s.p[(x,y)]
            # darker, slightly cooler shade of its own colour
            s.p[(x,y)]=(int(r*k*0.95),int(g*k),int(b*k*1.08) if b*k*1.08<255 else 255,255)
    def img(s):
        im=Image.new('RGBA',(16,16),(0,0,0,0))
        for (x,y),c in s.p.items(): im.putpixel((x,y),c)
        return im

def colshade(t):
    return 2 if t<0.12 else 4 if t<0.34 else 3 if t<0.56 else 2 if t<0.82 else 1

def can(P, x0,x1,y0,y1, metal, label, ly0, ly1, icon=None, ribs=True):
    w=x1-x0+1
    for x in range(x0,x1+1):
        t=(x-x0)/(w-1); k=colshade(t)
        for y in range(y0+1,y1+1):
            if ly0<=y<=ly1: c=label[k]
            else: c=metal[k]
            if ribs and not(ly0<=y<=ly1) and y not in (y0+1,y1) and (y-y0)%2==0: c=metal[max(0,k-1)]
            P.set(x,y,c)
    # lid ellipse
    for x in range(x0+1,x1): P.set(x,y0,metal[3])
    for x in range(x0+2,x1-1): P.set(x,y0+1,metal[4] if x<x0+w//2 else metal[3])
    P.set(x0+1,y0+1,metal[2]); P.set(x1-1,y0+1,metal[2])
    # bottom rim corners cut
    P.p.pop((x0,y1),None); P.p.pop((x1,y1),None)
    for x in range(x0+1,x1): P.set(x,y1,metal[1])
    if icon:
        cx=(x0+x1)//2; cy=(ly0+ly1)//2
        for (dx,dy,c) in icon: P.set(cx+dx,cy+dy,c)

def strip(P, A, B, hw, seg, jag=0.0, seed=1, crimp=None):
    rnd=random.Random(seed)
    ax,ay=A; bx,by=B; L=math.hypot(bx-ax,by-ay); ux,uy=(bx-ax)/L,(by-ay)/L; vx,vy=-uy,ux
    noise=[rnd.uniform(-jag,jag) for _ in range(40)]
    for y in range(16):
        for x in range(16):
            px,py=x+0.5-ax,y+0.5-ay; u=px*ux+py*uy; v=px*vx+py*vy
            t=u/L
            if t<0 or t>1: continue
            n=noise[int(t*39)]
            if abs(v)>hw+n: continue
            c=seg(t, v/(hw+n+1e-6), x, y)
            if c: P.set(x,y,c)

def grid(P, rows, cmap, shade=None):
    for y,row in enumerate(rows):
        assert len(row)==16,(row,len(row))
        for x,ch in enumerate(row):
            if ch=='.': continue
            c=cmap[ch]
            if isinstance(c,list):
                k=colshade((x-shade[0])/(shade[1]-shade[0])) if shade else 2
                c=c[k]
            P.set(x,y,c)

def mk_all():
    items={}
    tin=ramp('#a9adb3',spread=0.14); gold=ramp('#c79a3b'); 
    # 1 canned beans
    P=Px(); lab=ramp('#d8692a'); bean=ramp('#7a3b22')
    can(P,3,12,3,13,tin,lab,6,10,icon=[(-2,0,bean[2]),(-1,0,bean[3]),(0,-1,bean[2]),(1,-1,bean[3]),(1,1,bean[1]),(2,1,bean[2]),(-1,1,bean[1])])
    P.outline(); items['canned_beans']=P
    # 2 canned stew (тушёнка) short wide
    P=Px(); lab=ramp('#4f6a3a'); w=ramp('#e9dfc4')
    mt=ramp('#a8402c'); can(P,2,13,6,13,tin,lab,8,11,icon=[(-2,-1,mt[3]),(-1,-1,mt[3]),(0,-1,mt[2]),(1,-1,mt[2]),(-3,0,mt[2]),(-2,0,w[3]),(-1,0,w[3]),(0,0,w[2]),(1,0,mt[2]),(2,0,mt[1]),(-2,1,mt[1]),(-1,1,mt[1]),(0,1,mt[1]),(1,1,mt[0])])
    P.outline(); items['canned_stew']=P
    # 3 canned peaches
    P=Px(); lab=ramp('#e7c13d'); pe=ramp('#e2763a'); lf=ramp('#5f9c3a')
    can(P,3,12,3,13,tin,lab,6,10,icon=[(-1,0,pe[3]),(0,0,pe[2]),(1,0,pe[2]),(-1,1,pe[2]),(0,1,pe[2]),(1,1,pe[1]),(0,-1,pe[3]),(-1,-1,pe[4]),(1,-2,lf[3]),(2,-2,lf[2])])
    P.outline(); items['canned_peaches']=P
    # 4 condensed milk (blue / white)
    P=Px(); lab=ramp('#3a68b8'); wh=ramp('#eef0f2',spread=0.06)
    can(P,3,12,5,13,tin,lab,7,11)
    for x in range(3,13):
        k=colshade((x-3)/9); P.set(x,9,wh[k+0 if k<4 else 4])
    P.outline(); items['condensed_milk']=P
    # 5 energy drink slim can
    P=Px(); lab=ramp('#2b2f2c',spread=0.08); al=ramp('#b9c0c4'); y=ramp('#d9e83a')
    can(P,5,10,2,14,al,lab,4,13,ribs=False,icon=[(1,-3,y[3]),(0,-2,y[3]),(0,-1,y[4]),(-1,0,y[3]),(0,0,y[4]),(1,0,y[3]),(0,1,y[3]),(-1,2,y[2]),(-1,3,y[2])])
    P.outline(); items['energy_drink']=P
    # 6 bottled water
    P=Px(); cap=ramp('#2f62c4'); pl=ramp('#9fd4ea',spread=0.1); lb=ramp('#f2f5f7',spread=0.06); lb2=ramp('#3a8be0')
    for x in range(6,10):
        for yy in (1,2): P.set(x,yy,cap[3 if x==7 else 2])
    for x in range(6,10): P.set(x,3,pl[3 if x==7 else 2])
    for x in range(5,11): P.set(x,4,pl[3 if x in (6,7) else 2])
    for yy in range(5,15):
        for x in range(4,12):
            k=colshade((x-4)/7)
            c=pl[k]
            if 8<=yy<=11: c=lb[k] if yy!=10 else lb2[k]
            if yy in (6,13) and not(8<=yy<=11): c=pl[max(0,k-1)]
            P.set(x,yy,c)
    P.p.pop((4,14));P.p.pop((11,14))
    P.outline(); items['bottled_water']=P
    # 7 MRE pouch
    P=Px(); ol=ramp('#6b7340',spread=0.1); bk=ramp('#2e2f28',spread=0.05); tx=ramp('#c9c39a',spread=0.06)
    for yy in range(2,15):
        for x in range(3,13):
            t=(x-3)/9; k=3 if t<0.3 else 2 if t<0.8 else 1
            if yy in (2,3): k=min(4,k+1)
            if yy==2 and x%2==1: continue
            P.set(x,yy,ol[k])
    P.p.pop((12,4),None)  # tear notch
    for yy in range(7,12):
        for x in range(5,11): P.set(x,yy,bk[2])
    for x in range(6,10): P.set(x,8,tx[2])
    for x in range(6,9): P.set(x,10,tx[1])
    P.outline(); items['mre_ration']=P
    # 8 protein bar (diagonal wrapper)
    P=Px(); wr=ramp('#8e3fb0'); cr=ramp('#c6ccd2',spread=0.1); band=ramp('#f0c43a')
    def seg(t,v,x,y):
        k=4 if v<-0.45 else 3 if v<0.1 else 2 if v<0.6 else 1
        if t<0.1 or t>0.9:
            return cr[k] if (x+y)%2==0 else cr[max(0,k-1)]
        if 0.42<t<0.56: return band[k]
        return wr[k]
    strip(P,(2.2,13.8),(13.8,2.2),2.3,seg)
    P.outline(); items['protein_bar']=P
    # 9 hardtack (two crackers)
    P=Px(); ck=ramp('#d9b878',spread=0.1)
    for yy in range(5,14):
        for x in range(4,14): P.set(x,yy,ck[1])
    for yy in range(3,12):
        for x in range(2,12):
            k=3 if (x<4 or yy<5) else 2
            P.set(x,yy,ck[k])
    for (x,yy) in [(4,6),(7,6),(10,6),(4,9),(7,9),(10,9)]: P.set(x,yy,ck[0])
    P.outline(); items['hardtack']=P
    # 10 instant noodles cup
    P=Px(); cup=ramp('#c8342c',spread=0.07); wb=ramp('#ece4d2',spread=0.04); lid=ramp('#d4d7da',spread=0.1); nd=ramp('#e8c46a')
    for yy in range(5,15):
        inset=(yy-5)//4; x0,x1=3+inset,12-inset
        for x in range(x0,x1+1):
            k=colshade((x-x0)/max(1,x1-x0)); c=cup[k]
            if 8<=yy<=10: c=wb[k]
            P.set(x,yy,c)
    for x in range(2,14): P.set(x,4,lid[3])
    for x in range(3,13): P.set(x,3,lid[4] if x<8 else lid[3])
    P.set(1,2,lid[3]);P.set(2,2,lid[4]);P.set(2,3,lid[3])
    for x,yy in [(6,9),(7,8),(8,9),(9,8)]: P.set(x,yy,nd[2])
    P.outline(); items['instant_noodles']=P
    # 11 jerky
    P=Px(); mt=ramp('#7d3a22'); fat=ramp('#b8704a')
    def jseg(t,v,x,y):
        k=3 if v<-0.4 else 2 if v<0.4 else 1
        return (fat[2] if (x*7+y*3)%11==0 else mt[k])
    strip(P,(2.5,12.5),(12.5,3.0),1.7,jseg,jag=0.6,seed=3)
    strip(P,(4.5,14.2),(14.0,6.0),1.6,jseg,jag=0.6,seed=7)
    P.outline(); items['jerky']=P
    # 12 cured zombie jerky (rotten flesh, salted)
    P=Px(); zm=ramp('#6f7a3b'); salt=(236,236,228,255)
    def zseg(t,v,x,y):
        k=3 if v<-0.4 else 2 if v<0.4 else 1
        if (x*5+y*9)%13==0: return salt
        return zm[k] if (x+2*y)%7 else ramp('#7a4a2e')[2]
    strip(P,(2.5,12.5),(12.5,3.0),1.8,zseg,jag=0.7,seed=11)
    strip(P,(4.5,14.2),(14.0,6.0),1.6,zseg,jag=0.7,seed=5)
    P.outline(); items['zombie_jerky']=P
    # 13 rat on a stick
    P=Px(); st=ramp('#8a6236'); rat=ramp('#8c4f2c',spread=0.09); pk=ramp('#c98a7a')
    grid(P,["................",
            "..............s.",
            "..........pp.s..",
            ".........cddcs..",
            ".......cdeedkdc.",
            "......cdeeeddda.",
            ".....cdeeedddb..",
            "....cdeeeddcb...",
            "....cddddcccb...",
            "...pcbdccbbb....",
            "..p.sbbbbbb.....",
            "..p.s...........",
            ".p.s............",
            "..s.............",
            ".s..............",
            "................"],
         {'s':st[2],'p':pk[2],'a':rat[1],'b':rat[0],'c':rat[1],'d':rat[2],'e':rat[3],'k':(38,24,18,255)})
    P.outline(); items['grilled_rat']=P
    # 14 pickle jar
    P=Px(); brine=ramp('#cfc86a',spread=0.08); cu=ramp('#4e7d2c',spread=0.09); dl=ramp('#2f5a22')
    grid(P,["................",
            "................",
            "....gGGGGGGg....",
            "....gggggggg....",
            "....hyyyyyyy....",
            "...hyyCcyyyyy...",
            "...hyCCccyCcy...",
            "...hyCCccCCcy...",
            "...hyCCccCCcy...",
            "...hyCCccCCcy...",
            "...hyCCccCCcy...",
            "...hyyCcyCCcy...",
            "...hydyydCcyy...",
            "...hyyyyyyyyy...",
            "....yyyyyyyy....",
            "................"],
         {'g':gold[1],'G':gold[3],'h':(232,240,226,255),'y':brine,'C':cu[3],'c':cu[1],'d':dl[2]}, shade=(3,12))
    P.outline(); items['pickled_cucumbers']=P
    # 15 herbal tea in a glass bottle (Farmer's Delight drink style)
    P=Px(); cork=ramp('#9a6a3c',spread=0.08); gl=ramp('#cfe3e6',spread=0.07); tea=ramp('#9a7a2e',spread=0.08); lf=ramp('#5f9c3a')
    for yy in (1,2):
        for x in (7,8): P.set(x,yy,cork[3 if x==7 else 2])
    for yy in (3,4):
        for x in (7,8): P.set(x,yy,gl[3 if x==7 else 2])
    for x in range(5,11): P.set(x,5,gl[3 if x<8 else 2])
    for yy in range(6,15):
        for x in range(4,12):
            k=colshade((x-4)/7)
            c=tea[k] if yy>=8 and 4<x<11 else gl[k]
            P.set(x,yy,c)
    for yy in range(6,13): P.set(5,yy,(236,244,240,255))
    for x,yy in [(8,10),(9,9),(9,10),(10,9),(8,11)]: P.set(x,yy,lf[3] if yy<10 else lf[2])
    P.p.pop((4,14)); P.p.pop((11,14)); P.p.pop((4,6)); P.p.pop((11,6))
    P.outline(); items['herbal_tea']=P
    # 16 survivor's stew (Farmer's Delight style bowl)
    P=Px(); wd=ramp('#8a5a32',spread=0.07); stw=ramp('#9b4a2a'); car=ramp('#e2873a'); pot=ramp('#e2c98e'); hb=ramp('#5f9c3a')
    for yy in range(8,15):
        half=[6.5,6.5,6,5.5,4.8,4,3][yy-8]
        for x in range(16):
            if abs(x+0.5-8)<=half:
                t=(x+0.5-8+half)/(2*half); k=colshade(t)
                P.set(x,yy,wd[k] if yy>8 else wd[4])
    for yy in range(5,9):
        half=[4.5,6,6,6][yy-5]
        for x in range(16):
            if abs(x+0.5-8)<=half and yy<8: P.set(x,yy,stw[3 if yy==5 else 2])
    for x,yy,c in [(5,6,car[3]),(6,6,car[2]),(9,5,pot[3]),(10,6,pot[2]),(7,7,hb[3]),(11,7,car[2]),(4,7,pot[2]),(8,6,stw[4])]: P.set(x,yy,c)
    P.outline(); items['survivor_stew']=P
    # 17 chocolate ration (wrapper + foil + chocolate)
    P=Px(); wr=ramp('#5a6136',spread=0.1); foil=ramp('#cfd4d8',spread=0.12); ch=ramp('#5b3420')
    def cseg(t,v,x,y):
        k=4 if v<-0.45 else 3 if v<0.1 else 2 if v<0.6 else 1
        if t<0.52: return wr[k] if not(0.2<t<0.3) else ramp('#c9c39a')[k]
        if t<0.62: return foil[k] if (x+y)%2 else foil[max(0,k-1)]
        cc=ch[k]
        if int((t-0.62)*30)%3==2 or abs(v)<0.12: cc=ch[max(0,k-1)]
        return cc
    strip(P,(2.0,13.5),(13.8,2.3),2.4,cseg)
    P.outline(); items['chocolate_ration']=P
    return items


# ---------------------------------------------------------------- 31 more foods
def disc(P, cx, cy, rx, ry, rmp, light_from=(-0.4, -0.5), skip=None):
    for y in range(16):
        for x in range(16):
            dx, dy = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
            if dx * dx + dy * dy <= 1:
                l = dx * light_from[0] + dy * light_from[1]
                k = 4 if l > 0.55 else 3 if l > 0.1 else 2 if l > -0.45 else 1
                P.set(x, y, rmp[k])


def bottle_item(liquid, deco=(), fill=8, cork='#9a6a3c', glass='#cfe3e6'):
    P = Px(); ck = ramp(cork, spread=0.08); gl = ramp(glass, spread=0.07); lq = ramp(liquid, spread=0.08)
    for yy in (1, 2):
        for x in (7, 8): P.set(x, yy, ck[3 if x == 7 else 2])
    for yy in (3, 4):
        for x in (7, 8): P.set(x, yy, gl[3 if x == 7 else 2])
    for x in range(5, 11): P.set(x, 5, gl[3 if x < 8 else 2])
    for yy in range(6, 15):
        for x in range(4, 12):
            k = colshade((x - 4) / 7)
            P.set(x, yy, lq[k] if yy >= fill and 4 < x < 11 else gl[k])
    for yy in range(6, 13): P.set(5, yy, (236, 244, 240, 255))
    for x, yy, c in deco: P.set(x, yy, c)
    for c in ((4, 14), (11, 14), (4, 6), (11, 6)): P.p.pop(c, None)
    P.outline(); return P


def jar_item(brine, things, lid='#c79a3b'):
    P = Px(); g = ramp(lid); b = ramp(brine, spread=0.08)
    for x in range(4, 12):
        P.set(x, 2, g[3 if x < 8 else 2]); P.set(x, 3, g[1])
    for yy in range(4, 15):
        x0, x1 = (4, 11) if yy in (4, 14) else (3, 12)
        for x in range(x0, x1 + 1):
            P.set(x, yy, b[colshade((x - 3) / 9)])
    for x, yy, c in things: P.set(x, yy, c)
    for yy in range(5, 13): P.set(4, yy, (232, 240, 226, 255))
    P.outline(); return P


def bowl_item(content, chunks, mound=False):
    P = Px(); wd = ramp('#8a5a32', spread=0.07); st = ramp(content)
    for yy in range(8, 15):
        half = [6.5, 6.5, 6, 5.5, 4.8, 4, 3][yy - 8]
        for x in range(16):
            if abs(x + 0.5 - 8) <= half:
                t = (x + 0.5 - 8 + half) / (2 * half)
                P.set(x, yy, wd[colshade(t)] if yy > 8 else wd[4])
    rows = [(4, 3.0), (5, 5.0), (6, 6.0), (7, 6.0)] if mound else [(5, 4.5), (6, 6.0), (7, 6.0)]
    for yy, half in rows:
        for x in range(16):
            if abs(x + 0.5 - 8) <= half:
                P.set(x, yy, st[3 if yy == rows[0][0] else 2])
    for x, yy, c in chunks: P.set(x, yy, c)
    P.outline(); return P


def can_item(x0, x1, y0, y1, label, ly0, ly1, icon=None, ribs=True, metal='#a9adb3', extra=()):
    P = Px(); tin = ramp(metal, spread=0.14)
    can(P, x0, x1, y0, y1, tin, ramp(label, spread=0.08), ly0, ly1, icon=icon, ribs=ribs)
    for x, yy, c in extra: P.set(x, yy, c)
    P.outline(); return P


def stick_item(things):
    P = Px(); st = ramp('#8a6236')
    for i in range(14):
        x, yy = 1 + i, 14 - i
        P.set(x, yy, st[3]); P.set(x + 1, yy, st[1]) if i < 13 else None
    for f in things: f(P)
    P.outline(); return P


def mk_more():
    it = {}
    W = (240, 236, 226, 255)
    fish = ramp('#9fb6c8'); red = ramp('#c8342c'); mush = ramp('#8b5a3c'); cap_r = ramp('#c03a2a')
    it['canned_fish'] = can_item(2, 13, 7, 13, '#2f62c4', 9, 11, icon=[(-3, 0, fish[3]), (-2, 0, fish[3]), (-1, 0, fish[3]), (0, 0, fish[2]),
                                  (1, 0, fish[2]), (2, -1, fish[2]), (2, 1, fish[2]), (-2, -1, fish[4])])
    it['canned_tomato_soup'] = can_item(3, 12, 3, 13, '#c8342c', 6, 11,
                                        extra=[(x, 9, W) for x in range(4, 12)] + [(7, 7, (250, 210, 80, 255)), (8, 7, (250, 210, 80, 255))])
    it['canned_mushrooms'] = can_item(3, 12, 4, 13, '#6e4a2b', 7, 11, icon=[(-1, -1, cap_r[3]), (0, -1, cap_r[3]), (1, -1, cap_r[2]),
                                       (-2, 0, cap_r[2]), (-1, 0, W), (0, 0, cap_r[3]), (1, 0, cap_r[2]), (2, 0, cap_r[1]), (0, 1, W), (0, 2, W)])
    ham = ramp('#e08a8a')
    it['canned_ham'] = can_item(2, 13, 6, 13, '#d8a03a', 8, 11, icon=[(x, y, ham[3] if y < 0 else ham[2]) for x in range(-2, 3) for y in (-1, 0)] +
                                [(-3, 0, ham[1]), (3, 0, ham[1]), (0, 1, W), (1, 1, ham[1])])
    bone = ramp('#efe6cc')
    it['canned_dog_food'] = can_item(3, 12, 3, 13, '#e7c13d', 6, 11, icon=[(-2, -1, bone[3]), (-2, 1, bone[3]), (-1, 0, bone[3]), (0, 0, bone[3]),
                              (1, 0, bone[2]), (2, -1, bone[2]), (2, 1, bone[2])])
    it['cola'] = can_item(5, 10, 2, 14, '#b8231c', 4, 13, ribs=False, metal='#b9c0c4',
                          icon=[(-1, -2, W), (0, -1, W), (1, 0, W), (0, 1, W), (-1, 2, W), (0, 3, W)])
    leaf = ramp('#5f9c3a'); pine = ramp('#2f6a3a')
    it['instant_coffee'] = bottle_item('#4a2a18', deco=[(8, 7, (200, 170, 120, 255)), (9, 7, (200, 170, 120, 255))], fill=7)
    it['kvass'] = bottle_item('#7a4a1c', deco=[(x, 10, (226, 196, 120, 255)) for x in range(6, 11)] + [(8, 11, (150, 40, 30, 255))])
    it['moonshine'] = bottle_item('#dfe8e4', deco=[(6, 10, (60, 50, 40, 255)), (7, 11, (60, 50, 40, 255)), (8, 10, (60, 50, 40, 255)),
                                                   (9, 11, (60, 50, 40, 255)), (10, 10, (60, 50, 40, 255))], fill=7, glass='#d8e4ea')
    it['pine_needle_tea'] = bottle_item('#6b7a2e', deco=[(7, 10, pine[3]), (8, 9, pine[3]), (9, 10, pine[2]), (8, 11, pine[2]), (10, 9, pine[2])])
    yolk = (250, 200, 60, 255)
    it['pickled_eggs'] = jar_item('#d6cf86', [(x, y, W) for x, y in ((6, 6), (7, 6), (6, 7), (7, 7), (6, 8), (7, 8), (9, 8), (10, 8), (9, 9), (10, 9),
                                  (9, 10), (10, 10), (6, 11), (7, 11), (6, 12), (7, 12), (6, 13), (7, 13))] + [(7, 7, yolk)])
    kraut = ramp('#d8d088')
    it['sauerkraut'] = jar_item('#b8b870', [(x, y, kraut[3] if (x + y) % 3 == 0 else kraut[1]) for y in range(6, 14) for x in range(5, 12) if (x * 3 + y) % 4 == 0])
    it['marrow_soup'] = bowl_item('#d8b878', [(5, 6, bone[3]), (6, 6, bone[3]), (7, 6, bone[2]), (8, 6, bone[2]), (4, 5, bone[3]), (9, 5, bone[3]),
                                             (10, 7, leaf[2]), (11, 6, leaf[3])])
    gm = ramp('#7a3a22'); car = ramp('#e2873a'); pot = ramp('#e2c98e')
    it['game_stew'] = bowl_item('#8a4a26', [(5, 6, gm[1]), (6, 6, gm[1]), (9, 5, car[3]), (10, 6, car[2]), (4, 7, pot[2]), (7, 7, pot[3]),
                                            (11, 7, leaf[2]), (8, 5, gm[4])])
    dand = (250, 220, 60, 255)
    it['dandelion_salad'] = bowl_item('#5f9c3a', [(5, 4, dand), (9, 5, dand), (7, 6, dand), (11, 6, dand), (4, 6, leaf[4]), (8, 4, leaf[4]),
                                                  (10, 4, leaf[1]), (6, 5, leaf[1])], mound=True)
    it['porridge'] = bowl_item('#e8d8a8', [(7, 5, (255, 240, 200, 255)), (8, 5, (200, 160, 90, 255)), (9, 6, (200, 160, 90, 255)), (5, 6, (255, 240, 200, 255))])
    it['rice_gruel'] = bowl_item('#f0ead8', [(5, 6, car[3]), (8, 5, leaf[3]), (10, 6, car[2]), (6, 7, (250, 210, 80, 255)), (9, 7, leaf[2]),
                                             (11, 7, car[3]), (7, 4, (255, 250, 240, 255)), (8, 4, (255, 250, 240, 255))], mound=True)
    chili = ramp('#8e2a1e')
    it['bunker_chili'] = bowl_item('#a8301e', [(5, 6, chili[0]), (7, 6, chili[0]), (9, 5, chili[0]), (10, 7, chili[0]), (6, 5, (250, 220, 120, 255)),
                                               (8, 7, leaf[3])])
    it['scavenger_soup'] = bowl_item('#b8742e', [(5, 6, car[3]), (6, 6, car[2]), (9, 5, pot[3]), (10, 6, pot[2]), (7, 7, leaf[3]), (11, 7, leaf[2]),
                                                 (4, 7, ramp('#8ab04e')[3])])
    # rice crackers: two stacked round cakes with puffed grains
    P = Px(); rc = ramp('#e8dcb8', spread=0.07)
    disc(P, 8, 10.2, 6, 3.4, ramp('#cdbb8c', spread=0.07))
    disc(P, 8, 7.2, 6, 3.4, rc)
    for x, y in ((5, 6), (8, 5), (10, 7), (7, 8), (11, 6), (6, 7)): P.set(x, y, rc[1])
    P.outline(); it['rice_crackers'] = P
    # trail mix: a clear pouch of seeds, berries and cocoa
    P = Px(); bag = ramp('#dfe6e2', spread=0.06)
    for y in range(3, 14):
        for x in range(4, 12):
            if y == 3 and x % 2: continue
            P.set(x, y, bag[3 if y < 5 else colshade((x - 4) / 7)])
    rnd = random.Random(5)
    mixc = [(110, 70, 40, 255), (200, 40, 60, 255), (230, 220, 180, 255), (90, 140, 60, 255), (60, 40, 30, 255)]
    for y in range(6, 13):
        for x in range(5, 11):
            if rnd.random() < 0.75: P.set(x, y, mixc[rnd.randrange(len(mixc))])
    for x in range(4, 12): P.set(x, 5, bag[1])
    P.outline(); it['trail_mix'] = P
    # granola bar: open wrapper, oats and berries
    P = Px(); wr = ramp('#3e7a3a'); oat = ramp('#c8a060')
    def gseg(t, v, x, y):
        k = 4 if v < -0.45 else 3 if v < 0.1 else 2 if v < 0.6 else 1
        if t < 0.35: return wr[k] if not (0.12 < t < 0.2) else ramp('#e7c13d')[k]
        c = oat[k]
        if (x * 7 + y * 5) % 9 == 0: c = (150, 30, 50, 255)
        elif (x * 3 + y) % 5 == 0: c = oat[max(0, k - 1)]
        return c
    strip(P, (2.2, 13.8), (13.8, 2.2), 2.2, gseg)
    P.outline(); it['granola_bar'] = P
    # dried fruit: apricot halves and raisins
    P = Px(); ap_ = ramp('#e8902e'); rs = ramp('#5a2a3a')
    disc(P, 6, 6, 3.2, 2.6, ap_); disc(P, 10.5, 9.5, 3.2, 2.6, ap_); disc(P, 5.5, 11, 2.2, 1.8, rs); disc(P, 11, 4.5, 1.8, 1.6, rs)
    for x, y in ((6, 6), (10, 9)): P.set(x, y, ap_[1])
    P.outline(); it['dried_fruit'] = P
    # fish jerky
    P = Px(); fj = ramp('#b8907a')
    def fseg(t, v, x, y):
        k = 3 if v < -0.4 else 2 if v < 0.4 else 1
        return fish[3] if (x + y * 2) % 7 == 0 else fj[k]
    strip(P, (2.5, 12.5), (12.5, 3.0), 1.8, fseg, jag=0.5, seed=4)
    strip(P, (4.5, 14.2), (14.0, 6.0), 1.6, fseg, jag=0.5, seed=9)
    P.outline(); it['fish_jerky'] = P
    # roasted spider eye on a stick
    eye = ramp('#8e1e2a')
    it['roasted_spider_eye'] = stick_item([lambda P: disc(P, 10, 6, 2.6, 2.6, eye), lambda P: disc(P, 6.5, 9.5, 2.6, 2.6, eye),
                                           lambda P: P.set(9, 5, (250, 230, 200, 255)), lambda P: P.set(6, 9, (250, 230, 200, 255))])
    # boiled eggs: a whole egg and a halved one
    P = Px(); eg = ramp('#efe8dc', spread=0.06)
    disc(P, 6, 8, 3.2, 4.2, eg); disc(P, 10.5, 10, 3.4, 3.0, eg)
    disc(P, 10.5, 10, 1.6, 1.4, ramp('#f0b430'))
    P.outline(); it['boiled_eggs'] = P
    # pemmican: a dark block studded with berries
    P = Px(); pm = ramp('#5a3020')
    for y in range(5, 13):
        for x in range(3, 13):
            k = 4 if y == 5 else 3 if y == 6 else 1 if x == 12 or y == 12 else 2
            P.set(x, y, pm[k])
    for x, y in ((5, 8), (9, 7), (7, 10), (11, 9), (4, 11)): P.set(x, y, (170, 30, 50, 255))
    P.outline(); it['pemmican'] = P
    # hard candy: three wrapped sweets
    P = Px()
    for (cx, cy, col) in ((5, 5, '#d83a3a'), (10, 7, '#4aa84a'), (6, 11, '#e8b83a')):
        disc(P, cx + 0.5, cy + 0.5, 2.2, 2.2, ramp(col))
        for dx in (-3, 3):
            P.set(cx + dx, cy, W); P.set(cx + dx + (1 if dx > 0 else -1), cy - 1, W); P.set(cx + dx + (1 if dx > 0 else -1), cy + 1, W)
    P.outline(); it['hard_candy'] = P
    # mystery meat: grey-pink slab with suspicious green spots
    P = Px(); mm = ramp('#b88888')
    disc(P, 8, 8.5, 6, 4.2, mm)
    for x, y in ((6, 7), (10, 9), (8, 11), (11, 6)): P.set(x, y, (120, 150, 70, 255))
    for x in range(4, 12): P.set(x, 8, mm[4]) if x % 3 == 0 else None
    P.outline(); it['mystery_meat'] = P
    # emergency ration: a foil brick with an orange band
    P = Px(); fo = ramp('#c6ccd2', spread=0.1); ob = ramp('#e8742e')
    for y in range(4, 13):
        for x in range(2, 14):
            k = 4 if y == 4 else 3 if y < 7 else 1 if x == 13 or y == 12 else 2
            c = fo[k] if (x + y) % 3 else fo[max(0, k - 1)]
            if 7 <= y <= 9: c = ob[k]
            P.set(x, y, c)
    for x in range(4, 10): P.set(x, 8, (40, 40, 40, 255)) if x % 2 == 0 else None
    P.outline(); it['emergency_ration'] = P
    # mushroom skewer
    br = ramp('#a07050'); rc2 = ramp('#c03a2a')
    def caps(P):
        disc(P, 11, 4.5, 2.6, 1.8, rc2); disc(P, 7.5, 8, 2.6, 1.8, br); disc(P, 4.5, 11, 2.4, 1.7, rc2)
        for x, y in ((10, 4), (12, 5), (4, 11)): P.set(x, y, W)
    it['mushroom_skewer'] = stick_item([caps])
    return it


items=mk_all()
items.update(mk_more())
out=os.path.dirname(os.path.abspath(__file__)); os.makedirs(out+'/textures',exist_ok=True)
for n,P in items.items(): P.img().save(f'{out}/textures/{n}.png')

ru={'canned_beans':'Фасоль в томате','canned_stew':'Тушёнка','canned_peaches':'Консерв. персики','condensed_milk':'Сгущёнка',
'energy_drink':'Энергетик','bottled_water':'Бутылка воды','mre_ration':'Сухпаёк (ИРП)','protein_bar':'Протеиновый батончик',
'hardtack':'Галеты','instant_noodles':'Лапша быстр. пригот.','jerky':'Вяленое мясо','zombie_jerky':'Вяленая плоть зомби',
'grilled_rat':'Крыса на палочке','pickled_cucumbers':'Банка солений','herbal_tea':'Травяной чай',
'survivor_stew':'Похлёбка выжившего','chocolate_ration':'Армейский шоколад'}
ru.update({'canned_fish':'Рыбные консервы','canned_tomato_soup':'Томатный суп в банке','canned_mushrooms':'Грибы в банке','canned_ham':'Ветчина в банке','canned_dog_food':'Собачий корм в банке','cola':'Газировка','instant_coffee':'Растворимый кофе','kvass':'Квас','moonshine':'Самогон','pine_needle_tea':'Хвойный чай','marrow_soup':'Похлёбка из костей','game_stew':'Рагу из дичи','dandelion_salad':'Салат из одуванчиков','porridge':'Каша из пайка','rice_gruel':'Рисовая баланда','bunker_chili':'Чили из бункера','scavenger_soup':'Похлёбка мародёра','rice_crackers':'Рисовые хлебцы','trail_mix':'Походная смесь','granola_bar':'Гранола','dried_fruit':'Сухофрукты','fish_jerky':'Рыбная вяленка','roasted_spider_eye':'Жареный паучий глаз','boiled_eggs':'Варёные яйца','pemmican':'Пеммикан','hard_candy':'Леденцы','pickled_eggs':'Маринованные яйца','sauerkraut':'Квашеная капуста','mystery_meat':'Мясо неизвестного про.','emergency_ration':'Аварийный паёк','mushroom_skewer':'Грибной шашлык'})
try: font=ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf',15)
except: font=ImageFont.load_default()
S=8; cols=6; cell=170; names=list(items)
rows=(len(names)+cols-1)//cols
sheet=Image.new('RGBA',(cols*cell,rows*(cell+16)+10),(44,40,36,255)); d=ImageDraw.Draw(sheet)
for i,n in enumerate(names):
    cx=(i%cols)*cell; cy=(i//cols)*(cell+16)+8
    slot=Image.new('RGBA',(144,144),(139,139,139,255)); sd=ImageDraw.Draw(slot)
    sd.rectangle([0,0,143,7],fill=(55,55,55,255)); sd.rectangle([0,0,7,143],fill=(55,55,55,255))
    sd.rectangle([0,136,143,143],fill=(255,255,255,255)); sd.rectangle([136,0,143,143],fill=(255,255,255,255))
    im=items[n].img().resize((128,128),Image.NEAREST); slot.alpha_composite(im,(8,8))
    sheet.alpha_composite(slot,(cx+13,cy))
    tw=d.textlength(ru[n],font=font); d.text((cx+cell/2-tw/2,cy+148),ru[n],fill=(240,230,210,255),font=font)
sheet.save(f'{out}/preview_sheet.png')
# hotbar at real-ish scale x3
hb=Image.new('RGBA',(len(names)*20*3+6,22*3),(0,0,0,255)); 
for i,n in enumerate(names):
    s=Image.new('RGBA',(20,20),(139,139,139,255)); s.alpha_composite(items[n].img(),(2,2))
    hb.alpha_composite(s.resize((60,60),Image.NEAREST),(3+i*60,3))
hb.save(f'{out}/preview_hotbar_x3.png')
# cards: texture + name + what it gives
fx={'canned_beans':['Голод 6, насыщ. 0.6','Запас сил 3:00','→ пустая банка'],
'canned_stew':['Голод 8, насыщ. 0.8','Сила I 1:30','Запас сил 5:00'],
'canned_peaches':['Голод 5, насыщ. 0.5','Скорость I 1:00','Регенерация I 0:10'],
'condensed_milk':['Голод 4, насыщ. 0.4','Поглощение I 2:00','Спешка I 1:00'],
'energy_drink':['Голод 1, насыщ. 0.1','Адреналин 0:45','затем Отходняк 0:30'],
'bottled_water':['Голод 0','Регенерация I 0:05','снимает Отходняк, Голод, Тошноту'],
'mre_ration':['Голод 10, насыщ. 0.9','Запас сил 8:00','Сопротивление I 2:00'],
'protein_bar':['Голод 4, насыщ. 0.8','Сила I 0:45','ест за 0,8 с'],
'hardtack':['Голод 3, насыщ. 0.4','Запас сил 1:00','дешёвый крафт'],
'instant_noodles':['Голод 6, насыщ. 0.5','Регенерация I 0:15','Запас сил 2:00'],
'jerky':['Голод 6, насыщ. 0.7','Сила I 1:00','ест быстро'],
'zombie_jerky':['Голод 4, насыщ. 0.3','Мёртвый запах 2:00','Тошнота 0:05'],
'grilled_rat':['Голод 5, насыщ. 0.5','20%: Отравление 0:10','→ палка'],
'pickled_cucumbers':['Голод 3, насыщ. 0.3','снимает Отравление','и Тошноту'],
'herbal_tea':['Голод 2, насыщ. 0.2','ЛЕЧИТ ЗАРАЖЕНИЕ','Уют 1:00, Регенерация I'],
'survivor_stew':['Голод 10, насыщ. 0.8','Сопротивление I 3:00','Регенерация, Запас сил'],
'chocolate_ration':['Голод 5, насыщ. 0.6','Скорость I, Спешка I 1:30','Поглощение I 1:00']}
fx.update({'canned_fish':["Голод 6, насыщ. 0.6","Подводное дыхание I 1:00","Запас сил 2:00"],'canned_tomato_soup':["Голод 6, насыщ. 0.6","Уют 2:00",""],'canned_mushrooms':["Голод 5, насыщ. 0.5","Ночное зрение I 1:00",""],'canned_ham':["Голод 8, насыщ. 0.7","Сила I 1:00",""],'canned_dog_food':["Голод 4, насыщ. 0.2","30%: Голод 0:15",""],'cola':["Голод 2, насыщ. 0.2","Скорость I 0:30",""],'instant_coffee':["Голод 1, насыщ. 0.1","Спешка I 1:00",""],'kvass':["Голод 2, насыщ. 0.2","Запас сил 2:00",""],'moonshine':["Голод 1, насыщ. 0.1","Сопротивление I 1:00","Тошнота I 0:10"],'pine_needle_tea':["Голод 2, насыщ. 0.2","Уют 1:00","Регенерация I 0:05"],'marrow_soup':["Голод 4, насыщ. 0.4","Уют 2:00",""],'game_stew':["Голод 9, насыщ. 0.8","Сытость 3:00",""],'dandelion_salad':["Голод 4, насыщ. 0.4","Регенерация I 0:10",""],'porridge':["Голод 6, насыщ. 0.6","Уют 1:00",""],'rice_gruel':["Голод 5, насыщ. 0.5","Уют 1:00",""],'bunker_chili':["Голод 9, насыщ. 0.8","Сытость 2:00","Огнестойкость I 2:00"],'scavenger_soup':["Голод 8, насыщ. 0.7","Уют 3:00",""],'rice_crackers':["Голод 3, насыщ. 0.3","Запас сил 0:30",""],'trail_mix':["Голод 4, насыщ. 0.6","Скорость I 0:30",""],'granola_bar':["Голод 4, насыщ. 0.6","Спешка I 0:45",""],'dried_fruit':["Голод 3, насыщ. 0.4","Регенерация I 0:05",""],'fish_jerky':["Голод 5, насыщ. 0.6","Подводное дыхание I 0:30",""],'roasted_spider_eye':["Голод 2, насыщ. 0.2","Ночное зрение I 0:30","10%: Отравление 0:05"],'boiled_eggs':["Голод 4, насыщ. 0.4","Запас сил 0:30",""],'pemmican':["Голод 8, насыщ. 0.8","Запас сил 4:00",""],'hard_candy':["Голод 1, насыщ. 0.1","Скорость I 0:10",""],'pickled_eggs':["Голод 5, насыщ. 0.5","Сопротивление I 1:00",""],'sauerkraut':["Голод 4, насыщ. 0.4","Регенерация I 0:10","снимает Тошнота"],'mystery_meat':["Голод 6, насыщ. 0.4","30%: Голод 0:20",""],'emergency_ration':["Голод 6, насыщ. 0.8","Поглощение I 1:00","Запас сил 3:00"],'mushroom_skewer':["Голод 4, насыщ. 0.5","Ночное зрение I 0:20",""]})
try:
    fb=ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf',17); fs=ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf',14)
except Exception: fb=fs=font
cw,ch,cols=250,250,6; rows=(len(names)+cols-1)//cols
cards=Image.new('RGBA',(cols*cw+20,rows*ch+70),(38,34,30,255)); d=ImageDraw.Draw(cards)
d.text((20,14),'Еда для зомби-апокалипсиса — 17 предметов (16×16, показано ×6)',fill=(240,220,170,255),font=fb)
for i,n in enumerate(names):
    x=10+(i%cols)*cw; y=50+(i//cols)*ch
    d.rounded_rectangle([x+6,y,x+cw-6,y+ch-10],8,fill=(58,52,46,255))
    slot=Image.new('RGBA',(108,108),(139,139,139,255)); sd=ImageDraw.Draw(slot)
    sd.rectangle([0,0,107,5],fill=(55,55,55,255)); sd.rectangle([0,0,5,107],fill=(55,55,55,255))
    sd.rectangle([0,102,107,107],fill=(255,255,255,255)); sd.rectangle([102,0,107,107],fill=(255,255,255,255))
    slot.alpha_composite(items[n].img().resize((96,96),Image.NEAREST),(6,6))
    cards.alpha_composite(slot,(x+cw//2-54,y+10))
    t=ru[n]; tw=d.textlength(t,font=fb); d.text((x+cw/2-tw/2,y+124),t,fill=(250,240,220,255),font=fb)
    for j,line in enumerate(fx[n]):
        col=(150,220,150,255) if j else (200,190,170,255)
        if 'Отравление' in line and '%' in line or 'Тошнота' in line or 'Отходняк' in line and 'затем' in line: col=(230,140,120,255)
        if 'ЗАРАЖ' in line: col=(255,210,90,255)
        tw=d.textlength(line,font=fs); d.text((x+cw/2-tw/2,y+150+j*20),line,fill=col,font=fs)
cards.save(f'{out}/preview_cards.png')
print(len(items),'ok')


# ---- container (not in the preview): the empty can
def extras():
    tin=ramp('#a9adb3',spread=0.14)
    P=Px()
    can(P,4,11,5,13,tin,tin,0,-1)
    for x in range(6,10): P.set(x,6,tin[0])
    for (x,y) in [(10,4),(11,3),(12,2),(11,4),(12,3)]: P.set(x,y,tin[3])
    P.outline(); P.img().save(f'{out}/textures/empty_can.png')
extras()
print('extras ok')
