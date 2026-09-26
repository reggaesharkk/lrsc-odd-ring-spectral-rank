#!/usr/bin/env python3
"""Direct interval reconstruction of the passing theta=.07 K14 subset."""
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'k001-certificate'))
import lrsc_interval_certificate as cert

WITNESS=(0,1,2,4,5,6,42,43,44,45,46,47,48,49)

def main():
    cert.THETA=cert.I.rational(7,100)
    c,_,_,E,V,mask,_=cert.build()
    w=cert.score(E,V,WITNESS)
    assert sum(m.lo==cert.SCALE for m in mask)==83
    assert w.hi*10**6<c.lo
    print('K14 score interval at scale 1e35:',w.lo,w.hi)
    print('threshold numerator interval at scale 1e35 / 1e6:',c.lo,c.hi)
    print('upper relative residual:',(w.hi/c.lo)**.5)
    print('STATUS=PASS_DIRECT_INTERVAL_WITNESS')

if __name__=='__main__':main()
