# Certified minimum passing channel cardinality at the lower adjacent LRSC mask cell

For the LRSC v1.1.1 finite benchmark at \(M=99\), \(k_{\rm idx}=49\), \(A=1/2\), \(\theta=0.07\), and relative complex \(L_2\) tolerance \(10^{-3}\), the minimum passing channel cardinality is

\[
\boxed{K_{0.001}=14.}
\]

The same result holds for every \(\theta\in[0.055791974,0.071206343]\), where interval stress comparisons prove the mask stays at 83 active sites. The [prior adjacent-mask report](../adjacent-mask/REPORT.md) established only \(11\leq K_{0.001}\leq15\) in this cell. This certificate closes that gap. It applies to this specified finite model; it has no continuum Navier–Stokes implication.

## Passing witness

The subset \(S=\{0,1,2,4,5,6,42,43,44,45,46,47,48,49\}\) passes. Reconstructing the target and all selected complex Fourier vectors with the earlier rational outward-rounded interval engine gives, at scale \(10^{35}\),

\[
R(S)^2\in
[47866202293226631619166826454,\;
 47866202293226631619166826656].
\]

The applicable lower target norm squared is
\[
c\geq50451567155458613003131581499930492/10^{35}.
\]
The witness upper score is strictly less than \(10^{-6}\) times this lower \(c\). Its relative residual upper bound is \(0.0009740408151\). The assertions in `verify_witness.py` compare integers.

## Exclusion through 13

The [existing exact-integer exhaustive search](../adjacent-mask/mask_theta_07_search.txt) excludes \(K=1,\ldots,10\); the empty subset has residual norm \(\sqrt c\). For \(K=11,12,13\), this companion uses a necessary Fourier-coordinate condition to discard whole search branches while retaining outward rounding.

At each of the 198 real coordinates (real and imaginary parts of all 99 complex frequencies), `rigorous_coordinate_export.py` encloses the target \(E_d\) and each channel \(V_{i,d}\) by integer lower and upper endpoints at scale \(s=10^{14}\). For an increasing selected prefix \(P\), let \(f\) be the first permissible next index and \(r\) the remaining cardinality. Every completion's sum at coordinate \(d\) lies inside
\[
[L_d(f,r),U_d(f,r)],
\]
where \(L_d\) sums the \(r\) smallest lower endpoints among \(i\geq f\), and \(U_d\) sums the \(r\) largest upper endpoints. The required completion sum lies inside
\[
[E_{d,\mathrm{lo}}-P_{d,\mathrm{hi}},\;
 E_{d,\mathrm{hi}}-P_{d,\mathrm{lo}}].
\]
Let \(\delta_d\) be the nonnegative distance between these two integer intervals. Every completion satisfies
\[
s^2R^2\geq\sum_d\delta_d^2.
\]
The coefficient file's upper bound \(c_{\mathrm{hi}}\), scaled by \(10^{16}\), yields the outward upper acceptance threshold \(s^2 10^{-6}c\leq10^6c_{\mathrm{hi}}\). Thus a branch is safely rejected when the integer sum \(\sum_d\delta_d^2>10^6c_{\mathrm{hi}}\). Remaining leaves are checked against rigorous lower Gram scores. The program checks accumulator bounds before searching.

The recursion selects strictly increasing indices. At each rejected prefix it adds \(\binom{50-f}{r}\) to a coverage counter; at a leaf it adds one. The completed runs had **zero surviving leaves**, no cap reached, and these exact coverage totals:

| K | Search nodes | Covered subsets | Expected \(\binom{50}{K}\) |
| ---: | ---: | ---: | ---: |
| 11 | 4,404,636 | 37,353,738,800 | 37,353,738,800 |
| 12 | 17,122,820 | 121,399,651,100 | 121,399,651,100 |
| 13 | 59,726,649 | 354,860,518,600 | 354,860,518,600 |

In total, the coordinate gate accounts for **513,613,908,500** subsets across these cardinalities. `verify_coordinate_gate.py` separately checks the integer bound against 1,515 random and witness-prefix comparisons and confirms that the passing K=14 witness survives the necessary-condition filter at every level. That check is an implementation diagnostic; the mathematical branch inequality and completed coverage counters support the exclusion.

## Reproduction

From the repository root:

```sh
python3 finite-benchmark/theta07-rank14/rigorous_coordinate_export.py
python3 finite-benchmark/theta07-rank14/verify_coordinate_gate.py
python3 finite-benchmark/theta07-rank14/verify_witness.py
g++ -O3 -std=c++17 -Wall -Wextra finite-benchmark/theta07-rank14/rigorous_coordinate_search.cpp -o /tmp/lrsc-theta07-search
for k in 11 12 13; do
  /tmp/lrsc-theta07-search finite-benchmark/adjacent-mask/mask_theta_07_coefficients.txt finite-benchmark/theta07-rank14/mask_theta_07_coordinate_intervals.txt "$k" 200000000
done
```

The stored coordinate input has SHA-256 `aa9848207230ac8776d90869dfdcd74f383f4a80067f8a02846fdc9a53f49af7`. The output logs `rigorous_k11.txt`, `rigorous_k12.txt`, and `rigorous_k13.txt` record all depth counts and the completed status.


## Terminology note

The certified value (K_{0.001}=14) is a **minimum passing channel-subset
cardinality**, not the matrix rank from the odd-ring theorem. In this
(	heta=0.07) cell there are 42 active reflection orbits, so the separate
theorem quantity is (operatorname{rank}(V)=42). The historical directory
name `theta07-rank14` is retained only to preserve stable repository links.
