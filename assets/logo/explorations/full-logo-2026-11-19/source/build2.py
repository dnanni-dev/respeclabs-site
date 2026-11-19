import re,subprocess
from svgpathtools import parse_path
REPO='/home/claude/respeclabs-site/assets/logo/'
s=open(REPO+'no-slogan/svg/color-logo-no-background.svg').read()
seg=s[s.find('id="SvgjsG1773"'):]; word=re.findall(r'<path d="([^"]+)"',seg)[0]
subs=re.split(r'\s(?=M)',word)
bowl_orig=subs[0]; rest=' '.join(subs[1:])            # "ESPEC LABS"

# P: counter 8.04-11.58 and bowl bottom at 14.02, so its loop ends on the middle bar like the R
P_OLD_C="M27.04 8.04 l0 5.69998 l1.44 0 c0.12 0 0.19666 -0.02334 0.23 -0.07 s0.05 -0.12332 0.05 -0.22998 l0 -5.12"
P_NEW_C="M27.04 8.04 l0 3.54 l1.44 0 c0.12 0 0.19666 -0.02334 0.23 -0.07 s0.05 -0.12332 0.05 -0.22998 l0 -2.96"
P_OLD_O1="s0.43 0.74666 0.43 1.28 l0 6.94 c0 0.28"; P_NEW_O1="s0.43 0.74666 0.43 1.28 l0 4.82 c0 0.28"
P_OLD_O2="l-2.48 0 l0 3.86 l-2.88 0"; P_NEW_O2="l-2.48 0 l0 5.98 l-2.88 0"
# B: upper counter ends at 11.58 so the middle stroke sits exactly on the middle bar
B_OLD="M67.9 8.04 l0.00002 3.8 l1.36 0 c0.10666 0 0.19332 -0.03 0.25998 -0.09 s0.1 -0.15666 0.1 -0.29 l0 -3.14"
B_NEW="M67.9 8.04 l0.00002 3.54 l1.36 0 c0.10666 0 0.19332 -0.03 0.25998 -0.09 s0.1 -0.15666 0.1 -0.29 l0 -2.88"
E_OLD="l0 3.44 l2.4 0 l0 2.5 l-2.4 0 l0 3.16"; E_NEW="l0 3.38 l2.4 0 l0 2.44 l-2.4 0 l0 3.28"   # E middle arm on the middle bar (11.58-14.02)
rest=rest.replace(E_OLD,E_NEW); assert rest.count(E_NEW)==2
for a,b in [(P_OLD_C,P_NEW_C),(P_OLD_O1,P_NEW_O1),(P_OLD_O2,P_NEW_O2),(B_OLD,B_NEW)]:
    assert rest.count(a)==1,a; rest=rest.replace(a,b)
ws=open(REPO+'with-slogan/svg/color-logo-no-background.svg').read()
m=re.search(r'featureKey="mlRtrp-0"[^>]*>\s*<path d="([^"]+)"',ws); slogan=m.group(1)
def bbox(d):
    p=parse_path(d); x0,x1,y0,y1=p.bbox(); return x0,x1,y0,y1
RB=bbox(rest); SB=bbox(slogan)
print('rest',RB,'slogan',SB)
# ---- R mark (2B) in wordmark units ----
P=dict(bg='#100F16',tr='#23354A',bl='#4A86AB',go='#FFC24B',wh='#F2F2F2')
g=0.55; th=2.54; rh=(14.5-th-g*4)/4; sw=2.88*1.9; trw=sw*0.75
def bowl_path(x):  # aligned bowl (2B), its left edge at x
    top=5.5+th+g+rh+g; bot=top+rh; d=13.04-top; d2=15.38-bot; lh=20-bot; ox=1.52*lh/4.62; ix=1.4*lh/4.62
    dx=x-2.76
    pts=(f"M{8.06+dx:.4f} {14.1-d2:.4f} c0 0.32 -0.11 0.61334 -0.33 0.88 s-0.54334 0.4 -0.97 0.4 l{ox:.4f} {lh:.4f} L{3.88+ix+dx:.4f} 20 L{3.88+dx:.4f} {bot:.4f} L{x:.4f} {bot:.4f} L{x:.4f} {top:.4f} L{4.92+dx:.4f} {top:.4f} "
         f"c0.18666 0 0.28 -0.1 0.28 -0.3 l0 {-(4.4-d):.4f} c0 -0.2 -0.09334 -0.3 -0.28 -0.3 L{x:.4f} 8.04 L{x:.4f} 5.5 L{6.1+dx:.4f} 5.5 c0.68 0 1.17666 0.17 1.49 0.51 s0.47 0.79666 0.47 1.37 l0 {6.72-d2:.4f} z")
    return pts, 6.76+ox+dx
def corner(k): return f'c{-0.68*k:.3f} 0 {-1.17666*k:.3f} {-0.17*k:.3f} {-1.49*k:.3f} {-0.51*k:.3f} s{-0.47*k:.3f} {-0.79666*k:.3f} {-0.47*k:.3f} {-1.37*k:.3f}'
def rmark(x0, col=P, top='slant', foot='curve'):   # returns svg + right edge, in wordmark units, top at 5.5
    sx=x0+sw; stem=sx-trw; o=''; y0=5.5
    rows=[(y0+th+g+i*(rh+g)) for i in range(4)]   # top->bottom
    fills=[0.75,0.3,0.45,0.2]
    for i,(y,f) in enumerate(zip(rows,fills)):
        B=y+rh
        c45=sw-trw   # a true 45-degree cut, as wide as the serif's overhang
        if i==3 and foot=='curve': o+=f'<path d="M{stem:.3f} {y:.3f} L{sx:.3f} {y:.3f} L{sx:.3f} {B:.3f} L{stem+1.96:.3f} {B:.3f} {corner(1)} Z" fill="{col["tr"]}"/>'
        elif i==3 and foot=='slant':   # parallel to the serif's slant: same run per unit of height
            run=(sw-trw)/th*rh
            o+=f'<polygon points="{stem:.3f},{y:.3f} {sx:.3f},{y:.3f} {sx:.3f},{B:.3f} {stem+run:.3f},{B:.3f}" fill="{col["tr"]}"/>'
        elif i==3 and foot=='e':
            o+=f'<polygon points="{stem:.3f},{y:.3f} {sx:.3f},{y:.3f} {sx:.3f},{B:.3f} {stem+0.18518518518518517*rh:.3f},{B:.3f}" fill="{col["tr"]}"/>'
        elif i==3 and foot=='cut': o+=f'<polygon points="{stem:.3f},{y:.3f} {sx:.3f},{y:.3f} {sx:.3f},{B:.3f} {stem+c45:.3f},{B:.3f} {stem:.3f},{B-c45:.3f}" fill="{col["tr"]}"/>'
        else: o+=f'<rect x="{stem:.3f}" y="{y:.3f}" width="{trw:.3f}" height="{rh:.3f}" fill="{col["tr"]}"/>'
        o+=f'<rect x="{sx-sw*f:.3f}" y="{y:.3f}" width="{sw*f:.3f}" height="{rh:.3f}" fill="{col["bl"]}"/>'
    if top=='e':        # serif keeps its full length on top; the E's angle leaves a short flat underside before the stem
        o+=f'<polygon points="{x0:.3f},{y0} {sx:.3f},{y0} {sx:.3f},{y0+th} {x0+0.18518518518518517*th:.3f},{y0+th}" fill="{col["go"]}"/>'
    elif top=='e-stem': # same angle, ending exactly at the stem line (serif top slightly shorter)
        o+=f'<polygon points="{stem-0.18518518518518517*th:.3f},{y0} {sx:.3f},{y0} {sx:.3f},{y0+th} {stem:.3f},{y0+th}" fill="{col["go"]}"/>'
    elif top=='cut45': c=stem-x0; o+=f'<polygon points="{x0:.3f},{y0} {sx:.3f},{y0} {sx:.3f},{y0+th} {stem:.3f},{y0+th} {x0:.3f},{y0+th-c:.3f}" fill="{col["go"]}"/>'
    else: o+=f'<polygon points="{x0:.3f},{y0} {sx:.3f},{y0} {sx:.3f},{y0+th} {stem:.3f},{y0+th}" fill="{col["go"]}"/>'
    bp,right=bowl_path(sx+g); o+=f'<path d="{bp}" fill="{col["wh"]}"/>'
    return o,right
def svg(inner,vb,bg=None):
    x,y,w,h=vb; b=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x:.3f} {y:.3f} {w:.3f} {h:.3f}">{b}{inner}</svg>'
gap_orig=9.3-8.28
from retilt import retilt
rest6,nchg=retilt(rest,(sw-trw)/th); print('re-angled cuts:',nchg)
out={}
for key,top,foot in [('A1_slant_curve','slant','curve'),('A2_cut45_curve','cut45','curve'),('A3_cut45_cut45','cut45','cut'),('A4_slant_slant','slant','slant'),('A5_e_e','e','e'),('A5b_estem_e','e-stem','e'),('A6_slant_all','slant','slant')]:
    o,right=rmark(0,top=top,foot=foot); shift=right+gap_orig-RB[0]
    word=rest6 if key.startswith('A6') else rest
    out[key]=(o+f'<path d="{word}" fill="{P["wh"]}" transform="translate({shift:.4f},0)"/>',(0,5.5,RB[1]+shift,14.5))
for k,(inner,vb) in out.items():
    x,y,w,h=vb; pad=max(w,h)*0.08
    open(k+'.svg','w').write(svg(inner,(x-pad,y-pad,w+2*pad,h+2*pad),P['bg']))
    subprocess.run(['rsvg-convert','-h','400',k+'.svg','-o',k+'.png'],check=True)
