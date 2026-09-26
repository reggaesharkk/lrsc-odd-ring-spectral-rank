# LRSC fixed-point interval and exact-integer certificate

Research benchmark: Prince Upadhyay, LRSC v1.1.1, \(M=99\), \(k=49\), \(\theta=0.08\), \(A=0.5\). This is a new exploratory verification companion; the frozen releases remain unchanged.

Read `CERTIFICATE.md` for the claim, proof argument, complete output, commands, and computational trust boundary. Requires Python 3, NumPy, and a C++17 compiler. The `source/` directory contains the archived v1.1.1 operator source and recorded floating search log for comparison.

The verifier builds rational fixed-point intervals at scale \(10^{35}\). It encloses \(\pi\) using Machin's identity and alternating arctangent series, encloses sine and cosine by Taylor series with a proven remainder less than one grid unit, propagates outward-rounded integer intervals through the mask, DFT, channel construction and Gram coefficients, then compares the true enclosures to the exact rational values of the archived double coefficients. It independently bounds the directly reconstructed \(K=10\) selected subset and the explicit \(K=11\) witness. The latter **provably passes** relative residual \(0.001\) within the stated mathematical model.

The initial interval script still reports its **archived-log** check as conditional, with `all_K_le_10_certified_exclusion=false`. The new `exact_exhaustive.cpp` is a separate full run over all 13,432,735,555 subsets using rigorous integer lower-bound coefficients. Its output and its independent Python winner-score checker are included. A second bitmask algorithm independently repeats the decisive K=10 stage with the same result. Do not interpret the old field as the status of the completed exact-integer searches.

The output JSON records interval endpoints as **scaled integers**, so the critical comparisons can be reproduced without rounding decimal displays. The scalar widths shown as floats are diagnostics only; assertions and the witness test operate on integers or exact rational fractions.
