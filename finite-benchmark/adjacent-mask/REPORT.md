# A mask transition raises the LRSC fixed benchmark rank to 12

At \(M=99\), \(k_{\rm idx}=49\), \(A=1/2\), and relative complex \(L_2\) tolerance \(10^{-3}\), the minimum passing cardinality is **12 at \(\theta=0.09\)**. This is a finite, computer-assisted result for the channel construction in the [K=11 certificate](../k001-certificate/CERTIFICATE.md). The baseline at \(\theta=0.08\) has minimum 11. Moving the stress threshold across its first upper mask boundary therefore changes the certified minimum from 11 to 12.

## Mask cells and exact claims

| Stress threshold | Active nodes | Change from 0.08 | Certified cardinality |
| --- | ---: | --- | --- |
| 0.07 | 83 | add nodes 41 and 58 | \(11\leq K_{0.001}\leq15\) |
| 0.08 | 81 | baseline | \(K_{0.001}=11\) (prior certificate) |
| 0.09 | 79 | remove nodes 40 and 59 | **\(K_{0.001}=12\)** |

The \(\theta=0.09\) result holds on the closed rational subinterval
\([0.088346808,\,0.107144346]\), because every stress-mask decision remains unchanged there. The adjacent exact stress boundaries are approximately \(0.088346807373177\) and \(0.107144346727594\). Likewise, the \(\theta=0.07\) rank *range* holds on \([0.055791974,\,0.071206343]\). The endpoints of these stated rational subintervals are strictly separated from the corresponding stress levels by interval arithmetic. They are conservative subintervals of the complete mask cells.

## Certificate at 0.09

`interval_coefficients.py` reuses the rational outward-rounded construction in `../k001-certificate/lrsc_interval_certificate.py` at \(\theta=9/100\). This constructs all 50 channels and a target with integer interval arithmetic at scale \(10^{35}\), then exports lower bounds for \(c\), \(f_i\), and \(Q_{ij}\) at scale \(10^{16}\). For every subset \(S\), the resulting integer score is a rigorous lower bound on
\[
R(S)^2=c+\sum_{i\in S} f_i+\sum_{i,j\in S}Q_{ij}.
\]
The threshold is bounded above by the integer 5,003,948,331 at that scale.

`exact_search.cpp` enumerated every subset for cardinalities 1 through 10 and separately all \(\binom{50}{11}=37{,}353{,}738{,}800\) subsets at cardinality 11. Its recursion selects increasing channel indices, so each subset appears exactly once, and it checks each visited count against the corresponding binomial coefficient. It also checks a conservative 64-bit overflow bound before starting. The decisive result is:

| K | Visited | Minimum rigorous lower score | Upper threshold | Margin | Minimizing subset |
| ---: | ---: | ---: | ---: | ---: | --- |
| 10 | 10,272,278,170 | 6,159,983,416 | 5,003,948,331 | 1,156,035,085 | 0,1,3,6,44,45,46,47,48,49 |
| 11 | 37,353,738,800 | 5,015,646,197 | 5,003,948,331 | **11,697,866** | 0,1,3,42,43,44,45,46,47,48,49 |

All lower cardinalities also have strictly positive margins in `mask_theta_09_search.txt`. The empty subset has squared score \(c\), so it fails as well. `verify_search.py` independently recomputes every printed winner score in Python integers and checks all subset counts.

For the twelve-channel witness
\(S_{12}=\{0,1,3,41,42,43,44,45,46,47,48,49\}\), a *direct vector reconstruction* with the interval DFT gives
\[
10^{35}R(S_{12})^2\in
[44965520711298182576235681858,\;44965520711298182576235682058].
\]
The lower target squared norm is \(10^{35}c\geq50039483308509315172721015928750344\). Hence the upper witness score is strictly less than \(10^{-6}\) times this lower norm. Its displayed relative residual upper bound is \(0.000947945579\); the proof comparison uses integers, not this rounded display.

At \(\theta=0.07\), the exhaustive integer search excludes \(K\leq10\), and a directly reconstructed fifteen-channel witness \(\{0,1,3,11,12,13,14,42,43,44,45,46,47,48,49\}\) passes with relative residual upper bound \(0.000995214189\). The intermediate ranks 11 through 14 have **not** been excluded; no exact minimum is claimed for that cell.

## Reproduction

From the repository root:

```sh
python3 finite-benchmark/adjacent-mask/interval_coefficients.py 9
python3 finite-benchmark/adjacent-mask/interval_coefficients.py 7
g++ -O3 -std=c++17 -Wall -Wextra finite-benchmark/adjacent-mask/exact_search.cpp -o /tmp/lrsc-adjacent-search
/tmp/lrsc-adjacent-search finite-benchmark/adjacent-mask/mask_theta_09_coefficients.txt 1 10
/tmp/lrsc-adjacent-search finite-benchmark/adjacent-mask/mask_theta_09_coefficients.txt 11 11
/tmp/lrsc-adjacent-search finite-benchmark/adjacent-mask/mask_theta_07_coefficients.txt 1 10
python3 finite-benchmark/adjacent-mask/verify_search.py finite-benchmark/adjacent-mask/mask_theta_09_coefficients.txt finite-benchmark/adjacent-mask/mask_theta_09_search.txt
python3 finite-benchmark/adjacent-mask/verify_search.py finite-benchmark/adjacent-mask/mask_theta_09_coefficients.txt finite-benchmark/adjacent-mask/mask_theta_09_k11_search.txt
```

The stored search outputs are split by cardinality to make the decisive run explicit. Regenerated coefficient SHA-256 values are `613320d255dbb6200c70d4c82f78590bc713ebd44604f9f2e1fdd4016d523c72` at 0.09 and `e601007a5c00e47b0a1559cc2d890dc95122f3658ba551bafab53638393939d0` at 0.07. A separate floating FFT construction agrees on both masks and differs from the interval coefficients' endpoints by at most \(1.4\times10^{-14}\); this is an implementation cross-check, not the rigorous arithmetic basis.

This finite threshold transition does not establish any continuum Navier–Stokes regularity estimate, a theorem for other LRSC parameter choices, or the unresolved exact minimum at \(\theta=0.07\).
