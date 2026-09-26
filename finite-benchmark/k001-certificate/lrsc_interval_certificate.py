#!/usr/bin/env python3
"""Outward-rounded fixed-point verification for the M=99 LRSC benchmark.

No floating-point value is used to build an interval. Floating-point source
coefficients are compared through their exact as_integer_ratio representation.
This verifies coefficient enclosures and the K=11 witness; it does not rerun
the 13.4 billion-subset exclusion search.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import factorial, comb
from pathlib import Path
import json
import re
import sys

SCALE = 10**35
M = 99
K = 49
N = 50


def ceildiv(a: int, b: int) -> int:
    return -((-a) // b)


@dataclass(frozen=True)
class I:
    lo: int
    hi: int

    def __post_init__(self):
        assert self.lo <= self.hi

    @staticmethod
    def rational(a: int, b: int = 1) -> "I":
        assert b > 0
        return I(a * SCALE // b, ceildiv(a * SCALE, b))

    @staticmethod
    def fraction(x: Fraction) -> "I":
        return I.rational(x.numerator, x.denominator)

    def __add__(self, other: "I") -> "I":
        return I(self.lo + other.lo, self.hi + other.hi)

    def __neg__(self) -> "I":
        return I(-self.hi, -self.lo)

    def __sub__(self, other: "I") -> "I":
        return self + (-other)

    def __mul__(self, other: "I") -> "I":
        terms = (a * b for a in (self.lo, self.hi)
                 for b in (other.lo, other.hi))
        vals = tuple(terms)
        return I(min(vals) // SCALE, ceildiv(max(vals), SCALE))

    def divint(self, d: int) -> "I":
        assert d > 0
        return I(self.lo // d, ceildiv(self.hi, d))

    def square(self) -> "I":
        if self.lo <= 0 <= self.hi:
            low = 0
        else:
            low = min(self.lo * self.lo, self.hi * self.hi) // SCALE
        high = ceildiv(max(self.lo * self.lo, self.hi * self.hi), SCALE)
        return I(low, high)

    def width(self) -> float:
        return (self.hi - self.lo) / SCALE


ZERO = I(0, 0)
ONE = I(SCALE, SCALE)
HALF = I.rational(1, 2)
THETA = I.rational(8, 100)


def arctan_series(q: int, count: int) -> I:
    # Alternating arctan series; the next term encloses the tail.
    value = sum((Fraction((-1)**n, (2*n+1) * q**(2*n+1))
                 for n in range(count)), Fraction(0))
    next_term = Fraction(1, (2*count+1) * q**(2*count+1))
    lower = value-next_term if count % 2 else value
    upper = value if count % 2 else value+next_term
    return I(I.fraction(lower).lo, I.fraction(upper).hi)


def timesint(x: I, n: int) -> I:
    if n >= 0:
        return I(x.lo * n, x.hi * n)
    return -timesint(x, -n)


PI = timesint(arctan_series(5, 56), 16) - timesint(arctan_series(239, 25), 4)
assert PI.lo > 3*SCALE and PI.hi < 22*SCALE//7
assert Fraction(4**80, factorial(80)) < Fraction(1, SCALE)
assert Fraction(4**81, factorial(81)) < Fraction(1, SCALE)


def trig(n: int) -> tuple[I, I]:
    # n is a residue, moved to the principal interval [-49,49].
    n %= M
    if n > M//2:
        n -= M
    x = timesint(PI, 2*n).divint(M)
    assert -4*SCALE < x.lo <= x.hi < 4*SCALE
    x2 = x.square()
    cos_term = ONE
    sin_term = x
    cos_sum = ZERO
    sin_sum = ZERO
    for h in range(40):
        cos_sum = cos_sum + cos_term
        sin_sum = sin_sum + sin_term
        cos_term = -(cos_term*x2).divint((2*h+1)*(2*h+2))
        sin_term = -(sin_term*x2).divint((2*h+2)*(2*h+3))
    # Alternating-series tails have magnitude < 4^80/80!, 4^81/81!,
    # each strictly less than one grid unit. Enlarge by one unit per side.
    return I(cos_sum.lo-1, cos_sum.hi+1), I(sin_sum.lo-1, sin_sum.hi+1)


def zadd(z, w):
    return z[0]+w[0], z[1]+w[1]


def zmul(z, w):
    return z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0]


def zscale(z, r):
    return z[0]*r, z[1]*r


def zsq(z):
    return z[0].square()+z[1].square()


def zdot_real(z, w):
    return z[0]*w[0]+z[1]*w[1]


def zsum(seq):
    acc = (ZERO,ZERO)
    for z in seq:
        acc = zadd(acc,z)
    return acc


def build():
    roots = [trig(t) for t in range(M)]
    x = [ONE + HALF*roots[(K*i)%M][0] for i in range(M)]
    j = []
    stress = []
    for i in range(M):
        dl = x[i]-x[(i-1)%M]
        dr = x[i]-x[(i+1)%M]
        j.append(I(max(0,dl.lo,dr.lo),max(0,dl.hi,dr.hi)))
        stress.append(HALF*(dl.square()+dr.square()))
    assert all(s.lo>THETA.hi or s.hi<THETA.lo for s in stress)
    mask = [ONE if s.lo>THETA.hi else ZERO for s in stress]

    def dft(a):
        return [zscale(zsum(zscale((roots[(-q*i)%M][0],
                                    roots[(-q*i)%M][1]), a[i])
                            for i in range(M)), I.rational(1,M))
                for q in range(M)]

    hm, hj = dft(mask), dft(j)
    hy = dft([mask[i]*j[i] for i in range(M)])
    stencil = [roots[q][0]-ONE for q in range(M)]
    E = [zscale(hy[q], stencil[q]) for q in range(M)]
    V = []
    for r in range(N):
        if r==0:
            V.append([zscale(zmul(hj[0], hm[q]), stencil[q])
                      for q in range(M)])
        else:
            V.append([zscale(zadd(zmul(hj[r], hm[(q-r)%M]),
                                   zmul(hj[M-r], hm[(q+r)%M])), stencil[q])
                      for q in range(M)])
    c=zsum_real(zsq(z) for z in E)
    f=[timesint(zsum_real(zdot_real(V[r][q],E[q]) for q in range(M)), -2)
       for r in range(N)]
    Q=[[zsum_real(zdot_real(V[r][q],V[s][q]) for q in range(M))
        for s in range(N)] for r in range(N)]
    return c,f,Q,E,V,mask,stress


def zsum_real(seq):
    acc=ZERO
    for v in seq: acc=acc+v
    return acc


def within(interval: I, reference: float, radius: Fraction):
    n,d=reference.as_integer_ratio()
    return (Fraction(interval.lo,SCALE)>=Fraction(n,d)-radius and
            Fraction(interval.hi,SCALE)<=Fraction(n,d)+radius)


def score(E,V,indices):
    return zsum_real(zsq(zadd(E[q], zscale(zsum(V[i][q] for i in indices),I(-SCALE,-SCALE))))
                     for q in range(M))


def run():
    c,f,Q,E,V,mask,stress=build()
    source=Path(__file__).parent/'source'
    sys.path.insert(0,str(source))
    from audit_k1_to_k10 import operator_arrays
    *_,cd,fd,Qd=operator_arrays()
    rad=Fraction(1,10**10)
    assert within(c,cd,rad)
    assert all(within(f[i],float(fd[i]),rad) for i in range(N))
    assert all(within(Q[i][k],float(Qd[i,k]),rad) for i in range(N) for k in range(N))
    s11=(0,1,3,42,43,44,45,46,47,48,49)
    w=score(E,V,s11)
    assert w.hi*10**6<c.lo
    k10=(0,1,42,43,44,45,46,47,48,49)
    s10=score(E,V,k10)
    assert s10.lo*10**6>c.hi
    log=(source/'VERIFICATION_OUTPUT.txt').read_text()
    rows=re.findall(r'K=(\d+): expected=(\d+); visited=(\d+); best_subset=\((.*?)\); direct_error=([0-9.e+-]+);',log)
    assert len(rows)==10
    # The following is a check of an archived execution trace, not a new
    # certified exhaustive computation. Source review supplies traversal
    # coverage; the log itself cannot establish execution provenance.
    eps=Fraction(1,10**10)
    arithmetic_error=Fraction(1,10**9)
    norm_lower=Fraction(71029266,10**8) # 0.71029266, below measured norm
    c_upper=Fraction(c.hi,SCALE)
    log_margins=[]
    for cardinality,expected,visited,subset,reported in rows:
        k=int(cardinality)
        assert int(expected)==int(visited)==comb(50,k)
        d=Fraction(reported)
        # The source asserts 2e-12 agreement of Gram and direct residual.
        # Another 1e-16 covers formatting of the logged decimal.
        score_lower=(d-Fraction(2,10**12)-Fraction(1,10**16))**2*norm_lower**2
        margin=score_lower-arithmetic_error-(1+k+ k*k)*eps-Fraction(1,10**6)*c_upper
        assert margin>0
        log_margins.append(float(margin))
    report={
        'scope':'certified coefficient enclosures and selected witnesses; no certified full K<=10 search',
        'grid_scale':str(SCALE), 'pi_interval':[str(PI.lo),str(PI.hi)],
        'active_nodes':sum(m.lo==SCALE for m in mask),
        'min_stress_threshold_distance_lower':min(
            (s.lo-THETA.hi if s.lo>THETA.hi else THETA.lo-s.hi) for s in stress)/SCALE,
        'uniform_coefficient_radius':str(rad),
        'max_width_c':c.width(), 'max_width_f':max(t.width() for t in f),
        'max_width_Q':max(t.width() for row in Q for t in row),
        'K10_selected_score_scaled_integer_interval':[str(s10.lo),str(s10.hi)],
        'K11_witness_score_scaled_integer_interval':[str(w.lo),str(w.hi)],
        'threshold_score_scaled_integer_interval':[str(c.lo),str(c.hi), 'divide by 1e6'],
        'archived_search_counts_checked':True,
        'archived_search_minimum_remaining_margin':min(log_margins),
        'archived_search_status':'conditional on faithful full execution and asserted Gram/direct checks',
        'K11_certified_pass':True,
        'all_K_le_10_certified_exclusion':False,
    }
    print(json.dumps(report,indent=2))


if __name__=='__main__': run()
