#!/usr/bin/env python3
"""Export rigorous coefficient lower bounds at integer scale 10^16."""
from lrsc_interval_certificate import build, ceildiv, SCALE
from pathlib import Path
from hashlib import sha256

TARGET_SCALE = 10**16
RATIO = SCALE // TARGET_SCALE

def main():
    c, f, Q, *_ = build()
    values = [50, TARGET_SCALE, c.lo // RATIO, ceildiv(c.hi, RATIO)]
    values += [x.lo // RATIO for x in f]
    values += [x.lo // RATIO for row in Q for x in row]
    target = Path(__file__).with_name('integer_coefficients.txt')
    target.write_text('\n'.join(map(str, values))+'\n', encoding='ascii')
    print(target.name, 'sha256', sha256(target.read_bytes()).hexdigest())

if __name__=='__main__': main()
