#!/usr/bin/env python3
"""Independently recompute reported winner scores and check the result trace."""
import math
import re
from pathlib import Path
from lrsc_interval_certificate import build, SCALE, ceildiv

root=Path(__file__).parent
coeff=list(map(int,(root/'integer_coefficients.txt').read_text().split()))
assert len(coeff)==4+50+2500
n,scale,c_lo,c_hi=coeff[:4]
assert n==50 and scale==10**16
f=coeff[4:54]
Q=[coeff[54+50*i:104+50*i] for i in range(50)]
assert all(len(row)==50 for row in Q)
c,fi,qi,E,V,mask,stress=build()
ratio=SCALE//scale
assert c_lo==c.lo//ratio and c_hi==ceildiv(c.hi,ratio)
assert all(f[i]==fi[i].lo//ratio for i in range(50))
assert all(Q[i][j]==qi[i][j].lo//ratio for i in range(50) for j in range(50))
threshold=ceildiv(c_hi,10**6)
lines=(root/'exact_integer_search_output.txt').read_text().splitlines()
assert lines[-1]=='STATUS=PASS_EXACT_INTEGER_LOWER_BOUNDS'
assert len(lines)==12
for k,line in enumerate(lines[1:-1],start=1):
    match=re.fullmatch(r'K=(\d+); visited=(\d+); expected=(\d+); best_lower=(-?\d+); threshold_upper=(\d+); margin=(\d+); subset=([\d,]+)',line)
    assert match, line
    kk,visited,expected,best,limit,margin=map(int,match.groups()[:6])
    subset=tuple(map(int,match.group(7).split(',')))
    assert kk==k and len(subset)==k and len(set(subset))==k
    assert all(0<=i<50 for i in subset)
    assert visited==expected==math.comb(50,k)
    recomputed=c_lo+sum(f[i] for i in subset)+sum(Q[i][j] for i in subset for j in subset)
    assert best==recomputed and limit==threshold and margin==best-threshold>0
print('PASS: interval coefficients, counts, thresholds, and all reported winner scores independently checked')
print('CAVEAT: checking winners does not independently repeat the full traversal')
