#!/usr/bin/env python3
"""Certified theta plateau for the fixed M=99, k=49, A=1/2 benchmark."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "k001-certificate"))
from lrsc_interval_certificate import build, I, SCALE

LOW = I.rational(71206344, 10**9)  # 0.071206344
HIGH = I.rational(88346807, 10**9)  # 0.088346807


def main():
    *_, mask, stress = build()
    inactive = [(i, stress[i]) for i in range(len(mask)) if mask[i].lo == 0]
    active = [(i, stress[i]) for i in range(len(mask)) if mask[i].lo == SCALE]
    assert len(inactive) == 18 and len(active) == 81
    i_lo, highest_inactive = max(inactive, key=lambda item: item[1].hi)
    i_hi, lowest_active = min(active, key=lambda item: item[1].lo)
    assert highest_inactive.hi < LOW.lo
    assert lowest_active.lo > HIGH.hi
    print(f"max inactive at i={i_lo}: upper numerator={highest_inactive.hi} / {SCALE}")
    print(f"min active at i={i_hi}: lower numerator={lowest_active.lo} / {SCALE}")
    print("CERTIFIED: for every theta in [0.071206344, 0.088346807], the mask is identical to theta=0.08")
    print("COROLLARY: K_0.001=11 throughout this closed theta interval at fixed M=99, k_idx=49, A=0.5")


if __name__ == "__main__":
    main()
