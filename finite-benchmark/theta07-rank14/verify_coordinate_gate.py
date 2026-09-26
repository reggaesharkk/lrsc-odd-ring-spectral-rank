#!/usr/bin/env python3
"""Exact-integer spot check of the necessary Fourier-coordinate bound."""
from pathlib import Path
from math import comb
import random

N=50
K=14
WITNESS=(0,1,2,4,5,6,42,43,44,45,46,47,48,49)
ROOT=Path(__file__).resolve().parent

def load():
    items=list(map(int,(ROOT/'mask_theta_07_coordinate_intervals.txt').read_text().split()))
    assert items[:3]==[50,198,10**14] and len(items)==3+198*102
    rows=[]
    for d in range(198):
        v=items[3+102*d:3+102*(d+1)]
        rows.append((v[0],v[1],v[2::2],v[3::2]))
    c=list(map(int,(ROOT.parent/'adjacent-mask'/'mask_theta_07_coefficients.txt').read_text().split()))
    assert c[:2]==[50,10**16]
    return rows,c[3]*10**6

def bound(rows,threshold,prefix,first,r):
    total=0
    for tlo,thi,vlo,vhi in rows:
        required_lo=tlo-sum(vhi[i] for i in prefix)
        required_hi=thi-sum(vlo[i] for i in prefix)
        possible_lo=sum(sorted(vlo[first:])[:r])
        possible_hi=sum(sorted(vhi[first:],reverse=True)[:r])
        distance=max(0,possible_lo-required_hi,required_lo-possible_hi)
        total+=distance*distance
    return total

def main():
    rows,threshold=load()
    rng=random.Random(20260927)
    checks=0
    for subset in (WITNESS,*[tuple(sorted(rng.sample(range(N),K))) for _ in range(100)]):
        for depth in range(K+1):
            prefix=subset[:depth]
            first=prefix[-1]+1 if prefix else 0
            r=K-depth
            if N-first<r:continue
            lower=bound(rows,threshold,prefix,first,r)
            # Any specific completion lies inside every coordinate's optimistic
            # interval; its direct residual norm must dominate this lower bound.
            actual=0
            for tlo,thi,vlo,vhi in rows:
                residual_lo=tlo-sum(vhi[i] for i in subset)
                residual_hi=thi-sum(vlo[i] for i in subset)
                distance=max(0,residual_lo,-residual_hi)
                actual+=distance*distance
            assert lower<=actual
            if subset==WITNESS:assert lower<=threshold
            checks+=1
    print('PASS',checks,'integer prefix comparisons; witness survives all 15 levels')
    print('coverage targets',*[comb(50,k) for k in (11,12,13)])

if __name__=='__main__':main()
