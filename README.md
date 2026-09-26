# LRSC Odd-Ring Spectral Rank Theorem

**Prince Upadhyay — Independent Research**

This repository contains the frozen LRSC odd-ring spectral rank theorem, its
proof clarification, and a separate finite subset-selection certificate.

## Frozen rank theorem

Version 1.2 proves, for the specified single-step near-Nyquist local
redistribution map on an odd cyclic lattice and under the stated masking
conditions, that the rank of the conjugate-balanced post-stencil channel
family equals the number of active reflection orbits. This structural theorem
does **not** imply a universal fixed-unit compression number.

- Frozen theorem: [`odd-ring-rank-theorem/v1.2/`](odd-ring-rank-theorem/v1.2/)
- Proof clarification: [`odd-ring-rank-theorem/v1.2.1-supplement/`](odd-ring-rank-theorem/v1.2.1-supplement/)
- Frozen v1.2 OSF DOI: [10.17605/OSF.IO/NM5BW](https://doi.org/10.17605/OSF.IO/NM5BW)

The v1.2 materials remain frozen. The v1.2.1 supplement clarifies the proof
without replacing the archived theorem.

## Separate fixed-benchmark certificate

[`finite-benchmark/k001-certificate/`](finite-benchmark/k001-certificate/)
contains a reproducible computer-assisted certificate for one specified LRSC
instance: \(M=99\), \(k_{\rm idx}=49\), \(\theta=0.08\), \(A=0.5\). Its interval
construction and exact-integer searches exclude every subset of at most ten
channels at relative complex \(L_2\) error \(10^{-3}\); a directly enclosed
eleven-channel witness passes. Thus \(K_{0.001}=11\) **for this fixed instance**.

Read the [certificate and trust boundary](finite-benchmark/k001-certificate/CERTIFICATE.md)
before citing the result. The directory includes all source files, exported
integer coefficients, complete search outputs, hashes, and reproduction
commands. A [ZIP snapshot](finite-benchmark/k001-certificate/LRSC_K11_exact_integer_certificate_2026-09-26.zip)
is provided for convenience. The earlier [threshold error budget](finite-benchmark/THRESHOLD_ERROR_BUDGET.md)
records the prospective numerical margin analysis; the completed integer
certificate supersedes its then-open search task.

This finite benchmark does not establish a general LRSC compression theorem
or Navier–Stokes regularity. It is separate from the frozen v1.2 rank theorem.
