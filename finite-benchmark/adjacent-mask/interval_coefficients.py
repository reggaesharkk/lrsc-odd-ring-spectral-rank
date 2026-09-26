#!/usr/bin/env python3
"""Exploratory exact-interval coefficients for adjacent LRSC mask cells."""
import argparse
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'k001-certificate'))
import lrsc_interval_certificate as cert


def main():
    p = argparse.ArgumentParser()
    p.add_argument('theta', type=int, choices=(7, 9), help='theta in hundredths')
    args = p.parse_args()
    cert.THETA = cert.I.rational(args.theta, 100)
    c, f, q, e, v, mask, stress = cert.build()
    bounds = ((55791974, 71206343) if args.theta == 7
              else (88346808, 107144346))
    for endpoint in bounds:
        theta = cert.I.rational(endpoint, 10**9)
        assert all((m.lo == cert.SCALE and s.lo > theta.hi) or
                   (m.hi == 0 and s.hi < theta.lo) for s,m in zip(stress,mask))
    target_scale = 10**16
    ratio = cert.SCALE // target_scale
    vals = [50, target_scale, c.lo // ratio, cert.ceildiv(c.hi, ratio)]
    vals.extend(z.lo // ratio for z in f)
    vals.extend(z.lo // ratio for row in q for z in row)
    path = Path(__file__).resolve().parent / f'mask_theta_{args.theta:02d}_coefficients.txt'
    path.write_text('\n'.join(map(str, vals)) + '\n', encoding='ascii')
    old = (0, 1, 3, 42, 43, 44, 45, 46, 47, 48, 49)
    w = cert.score(e, v, old)
    print(f'theta={args.theta/100:.2f} active={sum(m.lo==cert.SCALE for m in mask)}')
    print('certified mask subinterval:', tuple(x/10**9 for x in bounds))
    print('changed indices:', [i for i,m in enumerate(mask) if (m.lo==cert.SCALE) != (stress[i].lo>cert.I.rational(8,100).hi)])
    print('old witness pass:', w.hi*10**6 < c.lo, 'relative residual upper:', (w.hi/c.lo)**0.5)
    witness = ((0,1,3,11,12,13,14,42,43,44,45,46,47,48,49) if args.theta == 7
               else (0,1,3,41,42,43,44,45,46,47,48,49))
    ws = cert.score(e, v, witness)
    assert ws.hi * 10**6 < c.lo
    print('passing witness:', witness)
    print('witness score interval:', ws.lo, ws.hi)
    print('threshold numerator interval:', c.lo, c.hi, '(divide by 1e6)')
    print('relative residual upper:', (ws.hi/c.lo)**0.5)
    print(path, hashlib.sha256(path.read_bytes()).hexdigest())


if __name__ == '__main__':
    main()
