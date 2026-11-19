import re,subprocess,sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from PIL import Image
F='/tmp/claude-0/-home-claude/08e627af-08e0-5afb-9602-5dc2859d494f/scratchpad/fonts/'
SRC='/tmp/claude-0/-home-claude/08e627af-08e0-5afb-9602-5dc2859d494f/scratchpad/lockup/final7/respeclabs-v7-logo-slogan-with-background.svg'
OUT='/tmp/claude-0/-home-claude/08e627af-08e0-5afb-9602-5dc2859d494f/scratchpad/sloganfonts/'
TEXT="IT'S TIME TO LEVEL UP"; L,R=13.009,83.779; TOP=22.2; CAP=2.61
fonts={'current':None,
 'chakra-petch':F+'fontsource-chakra-petch-5.3.0/package/files/chakra-petch-latin-600-normal.woff',
 'oxanium':F+'fontsource-oxanium-5.3.0/package/files/oxanium-latin-600-normal.woff',
 'rajdhani':F+'fontsource-rajdhani-5.3.0/package/files/rajdhani-latin-700-normal.woff',
 'michroma':F+'fontsource-michroma-5.3.0/package/files/michroma-latin-400-normal.woff'}
base=open(SRC).read()
m=re.search(r'<path d="[^"]+"[^>]*transform="translate\([^)]*\) scale\(0\.18\d*\)"/>',base)
for name,fp in fonts.items():
    if fp:
        f=TTFont(fp); gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm
        cap=getattr(f['OS/2'],'sCapHeight',0) or 0
        if not cap:
            bp=BoundsPen(gs); gs[cmap[ord('H')]].draw(bp); cap=bp.bounds[3]
        sc=CAP/cap
        # glyph ink bounds and advances
        items=[]
        for ch in TEXT:
            g=cmap[ord(ch)]; bp=BoundsPen(gs); gs[g].draw(bp)
            items.append((g,gs[g].width,bp.bounds))
        # natural ink width from first ink left to last ink right with advances
        n=len(TEXT)-1
        x=0; pos=[]
        for g,adv,b in items: pos.append(x); x+=adv
        inkL=items[0][2][0]; inkR=pos[-1]+items[-1][2][2]
        nat=(inkR-inkL)*sc; track=((R-L)-nat)/n/sc  # extra font units per gap
        d=''
        for i,(g,adv,b) in enumerate(items):
            ox=pos[i]+i*track-inkL
            pen=SVGPathPen(gs)
            tp=TransformPen(pen,(sc,0,0,-sc,L+ox*sc,TOP+cap*sc))
            gs[g].draw(tp); d+=pen.getCommands()
        s=base.replace(m.group(0),f'<path d="{d}" fill="#999999"/>')
    else: s=base
    open(OUT+name+'.svg','w').write(s)
    subprocess.run(['rsvg-convert','-w','2000',OUT+name+'.svg','-o',OUT+name+'.png'],check=True)
    print(name)
