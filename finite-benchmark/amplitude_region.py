#!/usr/bin/env python3
"""Exact rational parameter-region checks for the fixed M=99, k_idx=49 LRSC."""
from fractions import Fraction
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "k001-certificate"))
from lrsc_interval_certificate import build, SCALE


def main():
    *_, mask, stress = build()  # baseline A=1/2, theta=0.08
    inactive_hi = max(stress[i].hi for i in range(99) if mask[i].lo == 0)
    active_lo = min(stress[i].lo for i in range(99) if mask[i].lo == SCALE)

    def scaled_stress(a: Fraction, numerator: int) -> Fraction:
        return 4*a*a*Fraction(numerator, SCALE)

    theta = Fraction(8, 100)
    a_lo, a_hi = Fraction(475795, 10**6), Fraction(529975, 10**6)
    assert scaled_stress(a_lo, active_lo) > theta
    assert scaled_stress(a_hi, inactive_hi) < theta

    r_lo, r_hi = Fraction(49, 100), Fraction(51, 100)
    t_lo, t_hi = Fraction(74084, 10**6), Fraction(84848, 10**6)
    assert scaled_stress(r_hi, inactive_hi) < t_lo
    assert scaled_stress(r_lo, active_lo) > t_hi
    print("CERTIFIED A INTERVAL: [0.475795, 0.529975] at theta=0.08")
    print("CERTIFIED RECTANGLE: A in [0.49, 0.51], theta in [0.074084, 0.084848]")
    print("In the wider sufficient region, require 4*A^2*inactive_hi/SCALE <= theta < 4*A^2*active_lo/SCALE")
    print("MASK SAME; all target/channel vectors scale by A; K_0.001=11 throughout")


if __name__ == "__main__":
    main()
