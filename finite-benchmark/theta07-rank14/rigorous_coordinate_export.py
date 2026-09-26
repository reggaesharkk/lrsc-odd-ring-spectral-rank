#!/usr/bin/env python3
"""Outward-rounded integer Fourier coordinates for the theta=.07 search."""
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'k001-certificate'))
import lrsc_interval_certificate as cert

SCALE = 10**14
RATIO = cert.SCALE // SCALE


def main():
    cert.THETA = cert.I.rational(7,100)
    c, _, _, E, V, mask, _ = cert.build()
    rows=[]
    for q in sorted(range(cert.M),key=lambda n: n*(cert.M-n),reverse=True):
        for component in range(2):
            target=E[q][component]
            channels=[V[i][q][component] for i in range(cert.N)]
            vals=[target.lo//RATIO,cert.ceildiv(target.hi,RATIO)]
            for z in channels:
                vals.extend((z.lo//RATIO,cert.ceildiv(z.hi,RATIO)))
            rows.append(vals)
    assert len(rows)==198
    dest=Path(__file__).with_name('mask_theta_07_coordinate_intervals.txt')
    with dest.open('w') as output:
        output.write(f'{cert.N} {len(rows)} {SCALE}\n')
        for row in rows:output.write(' '.join(map(str,row))+'\n')
    print(dest,'active',sum(m.lo==cert.SCALE for m in mask),'c_upper_1e14',cert.ceildiv(c.hi,RATIO))


if __name__=='__main__':main()
