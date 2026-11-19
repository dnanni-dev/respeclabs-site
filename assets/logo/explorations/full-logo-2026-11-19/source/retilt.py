# Re-angle the wordmark's short terminal cuts (the 0.5-across / 2.7-down slants on E, S, C, L, B, P ends)
# to the R mark's serif angle, keeping each letter's outermost corner fixed.
from svgpathtools import parse_path, Line
RATIO=None
def retilt(d, ratio, cap=5.5, base=20.0, tol=0.02):
    path=parse_path(d); changes=[]
    for seg in path:
        if isinstance(seg,Line):
            dx=seg.end.real-seg.start.real; dy=seg.end.imag-seg.start.imag
            if 0.4<abs(dx)<0.6 and 2.5<abs(dy)<2.9:
                pts=[seg.start,seg.end]
                outer=[p for p in pts if abs(p.imag-cap)<tol or abs(p.imag-base)<tol]
                if len(outer)!=1: continue
                po=outer[0]; pi=pts[1] if po==pts[0] else pts[0]
                newx=pi.real+(po.real-pi.real)/abs(po.real-pi.real)*abs(dy)*ratio
                changes.append((po,complex(newx,po.imag)))
    for old,new in changes:
        for seg in path:
            for attr in ('start','end'):
                if abs(getattr(seg,attr)-old)<1e-6: setattr(seg,attr,new)
    return path.d(), len(changes)
