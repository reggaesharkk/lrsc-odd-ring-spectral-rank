# 13 Billion to One — exact-arithmetic research challenge

**Live content:** `docs/challenge/index.html` plus the dataset `docs/challenge/data.js`.

This static browser experience is a user-facing explanation and challenge surface based on the **specific published LRSC M=99, k-index=49, theta=0.08, A=0.5 finite benchmark**, with relative complex L2 tolerance 1e-3. It is not a new continuum theorem, not a proof assistant, and not an unconditional result about zeta or Navier–Stokes.

- Up to 10 selected channels: the original exact integer search (13,432,735,555 nonempty subsets) certifies that **none** reaches the target, with a separate independent bitmask check of the 10-channel layer.
- Precisely one **exhibited** 11-channel set has a separate rigorous interval-enclosed success witness. Other 11-channel selections are **not** labeled successes from the mere lower bound.
- The browser evaluates a rigorous integer **lower score** for any chosen subset using `BigInt`, replays the archived 10 best-subset score records, checks the total combination count, and (where WebCrypto is available) checks SHA-256 of the frozen coefficient file. It **does not** rerun the 13.4 billion exhaustive leaves.
- Original source and independent replication: [canonical certificate](https://github.com/reggaesharkk/lrsc-odd-ring-spectral-rank/blob/main/finite-benchmark/k001-certificate/CERTIFICATE.md); coefficient SHA-256 `e10cc9fe85c538b3357bb3a4d180ebedf915b86a27f9d4c6bb248ab882d6fc24`.

No external framework, API, paid service or user login. `data.js` contains the published canonical coefficient file embedded as text; it is not a simulation.

**GitHub Pages:** Set Settings > Pages > Deploy from branch `main`, directory `/docs`, to serve the challenge at `/challenge/`. Check existing Pages settings before modifying them.

**Rights and claims:** scoped author-owned original expression policy applies; no claim is made of first-ever game design or mathematically verified originality.
