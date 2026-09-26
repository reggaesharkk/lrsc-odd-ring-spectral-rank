#!/usr/bin/env python3
"""Independently recompute reported winners from rigorous integer bounds."""
import argparse
import math
import re
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('coefficients', type=Path)
    ap.add_argument('search_output', type=Path)
    args = ap.parse_args()
    v = list(map(int, args.coefficients.read_text().split()))
    assert len(v) == 2554 and v[0] == 50 and v[1] == 10**16
    c_lo, c_hi = v[2:4]
    f = v[4:54]
    q = [v[54+50*i:104+50*i] for i in range(50)]
    threshold = (c_hi + 999999)//1000000
    rows = re.findall(r'K=(\d+); visited=(\d+); expected=(\d+); best_lower=(-?\d+); threshold_upper=(\d+); margin=(-?\d+); subset=([\d,]+)', args.search_output.read_text())
    assert rows
    for k_text, visited, expected, best, limit, margin, subset in rows:
        k = int(k_text)
        indices = tuple(map(int, subset.split(',')))
        assert len(indices) == k and tuple(sorted(set(indices))) == indices
        assert int(visited) == int(expected) == math.comb(50,k)
        exact = c_lo + sum(f[i] for i in indices) + sum(q[i][j] for i in indices for j in indices)
        assert exact == int(best) and int(limit) == threshold
        assert exact-threshold == int(margin)
        print(k, 'visited', visited, 'best lower', exact, 'margin', margin)
    print('PASS: all reported winner scores and binomial counts recomputed')


if __name__ == '__main__':
    main()
