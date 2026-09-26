# Finite LRSC threshold certificate — fixed M=99 benchmark

**Research author:** Prince Upadhyay. **Verification supplement:** 26 September 2026. This package leaves the frozen LRSC releases unchanged.

## Claim and precise scope

For the LRSC channel decomposition defined by the included v1.1.1 operator source at \(M=99\), \(k_{\rm idx}=49\), \(\theta=0.08\), and \(A=0.5\), the smallest subset cardinality achieving relative complex \(L_2\) error at most \(10^{-3}\) is **11**. This is a finite, computer-assisted certificate for one specified benchmark. It makes no claim about a continuum Navier–Stokes equation, other LRSC parameters, or literature novelty.

## Proof structure

The mathematical target \(E\in\mathbb C^{99}\) and 50 paired channels \(V_i\) satisfy, for a subset \(S\),

\[
\left\|E-\sum_{i\in S}V_i\right\|_2^2
=c+\sum_{i\in S}f_i+\sum_{i,j\in S}Q_{ij},\quad
c=\|E\|_2^2,\quad f_i=-2\Re\langle V_i,E\rangle,\quad Q_{ij}=\Re\langle V_i,V_j\rangle.
\]

`lrsc_interval_certificate.py` encloses \(\pi\) by Machin's arctangent identity and alternating rational series. Sine and cosine use Taylor polynomials on \([-4,4]\) with rationally verified remainder less than one unit at scale \(10^{35}\). Every interval operation rounds outward through integer floor/ceiling. It encloses all mask decisions, the DFT, target, channels, and Gram coefficients. The mask has 81 active nodes. No floating value is used to produce the intervals.

`export_integer_coefficients.py` rounds **down** each \(c,f_i,Q_{ij}\) interval endpoint to integer scale \(B=10^{16}\), except that it rounds the upper endpoint of \(c\) **up**. Therefore every subset has a rigorous integer lower score \(L(S)\), and the pass threshold has rigorous integer upper bound \(U=5{,}045{,}156{,}716\). A valid exclusion is \(\min_{|S|=K} L(S)>U\).

`exact_exhaustive.cpp` enumerates each increasing \(K\)-tuple exactly once. At each depth the next index runs from the first eligible index through \(50-(K-\mathrm{depth})\). By induction this is a bijection to the \(\binom{50}{K}\) subsets. The program checks that count, checks a conservative absolute bound of \(509{,}144{,}783{,}408{,}693{,}451 < 2^{63}-1\) before the traversal, and uses integer additions only in its score updates. The leaf score is exactly \(c_\downarrow+\sum f_{i,\downarrow}+\sum_{i,j}Q_{ij,\downarrow}\). Since all coefficients are componentwise lower bounds, this leaf score is at most the true score multiplied by \(B\), apart from the harmless interpretation of the fixed integer scale.

| K | Enumerated subsets | Minimum integer lower score | Margin over U |
|---:|---:|---:|---:|
| 0 | 1 | at least the exported \(c_\downarrow\) | positive |
| 1 | 50 | 2,952,642,845,575 | 2,947,597,688,859 |
| 2 | 1,225 | 2,379,085,141,606 | 2,374,039,984,890 |
| 3 | 19,600 | 366,998,862,903 | 361,953,706,187 |
| 4 | 230,300 | 31,540,087,314 | 26,494,930,598 |
| 5 | 2,118,760 | 29,380,496,243 | 24,335,339,527 |
| 6 | 15,890,700 | 17,727,554,553 | 12,682,397,837 |
| 7 | 99,884,400 | 15,193,292,406 | 10,148,135,690 |
| 8 | 536,878,650 | 8,560,399,866 | 3,515,243,150 |
| 9 | 2,505,433,700 | 7,143,182,466 | 2,098,025,750 |
| 10 | 10,272,278,170 | **5,454,959,195** | **409,802,479** |

In total the run visited **13,432,735,555** nonempty subsets through \(K=10\). The separate `check_exact_output.py` recomputes exported coefficient bounds and every printed winning subset score in Python exact integers. It checks the counts and margins, but does not itself repeat all 13.4 billion leaves.

### Independent decisive-stage replication

`independent_bitmask_check.cpp` separately enumerates every fixed-popcount 50-bit mask at \(K=10\) using Gosper's successor rule. It updates the exact score as channels leave and enter the mask and recomputes a direct score every 100 million masks. Its completed output agrees exactly with the lexicographic recursion: **10,272,278,170** masks, best lower score **5,454,959,195**, threshold upper **5,045,156,716**, and winner \(\{0,1,42,43,44,45,46,47,48,49\}\). This checks the decisive enumeration through a distinct traversal and scoring algorithm using the same independently enclosed coefficient file. The earlier recursive run covers \(K=1,\ldots,9\).

For \(S_{11}=\{0,1,3,42,43,44,45,46,47,48,49\}\), the interval verifier directly encloses the residual norm squared at integer grid scale \(10^{35}\):

\[
R(S_{11})^2\in[46725937774006983998256510624,
46725937774006983998256510826]/10^{35}.
\]

The threshold \(10^{-6}c\) lies between

\[
[50451567155458613003131581499930492,
50451567155458613003131581499931196]/10^{41}.
\]

The upper witness score is strictly below the lower threshold. This proves a pass at \(K=11\) and the integer exclusion proves no pass at \(K\leq10\).

## Reproduction and trust boundary

From the package directory, run:

```sh
python3 lrsc_interval_certificate.py
python3 export_integer_coefficients.py
g++ -O3 -std=c++17 -Wall -Wextra exact_exhaustive.cpp -o exact_exhaustive
./exact_exhaustive integer_coefficients.txt 10 | tee exact_integer_search_output.txt
python3 check_exact_output.py
g++ -O3 -std=c++17 -Wall -Wextra independent_bitmask_check.cpp -o independent_bitmask_check
./independent_bitmask_check integer_coefficients.txt | tee independent_bitmask_output.txt
sha256sum -c SHA256SUMS.txt
```

The complete searches may take minutes depending on hardware. The result is a reproducible **computer-assisted proof**, not a proof-assistant-checked derivation. It assumes correct execution of the supplied Python/C++ sources, arbitrary-precision Python integer arithmetic, C++ signed integer arithmetic within the checked bound, and the mathematical validity of the documented interval and traversal arguments. The two exact-integer algorithms independently check the decisive search, but they share one generated coefficient file. Formal code verification or an unrelated interval implementation would further strengthen implementation assurance.
