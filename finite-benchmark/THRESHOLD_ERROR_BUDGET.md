# LRSC fixed benchmark: a threshold robustness gate

**Exploratory note, 26 September 2026.** This note does not amend the frozen LRSC releases. It isolates a finite mathematical certification task from the established numerical benchmark. It does not claim a solution to a continuum Navier–Stokes problem.

## Fixed question

For the published LRSC benchmark \(M=99\), \(k=49\), \(\theta=0.08\), \(A=0.5\), let \(E\in\mathbb C^{99}\) be the target and \(V_0,\ldots,V_{49}\in\mathbb C^{99}\) the conjugate-balanced channels, as defined in `LRSC_v1_1_1_Source_Bundle.zip`. For a subset \(S\), set

\[
R(S)^2=\left\|E-\sum_{i\in S}V_i\right\|_2^2
=c+\sum_{i\in S} f_i+\sum_{i,j\in S}Q_{ij},\quad
c=\|E\|_2^2,\quad f_i=-2\operatorname{Re}\langle V_i,E\rangle,\quad
Q_{ij}=\operatorname{Re}\langle V_i,V_j\rangle.
\]

The decision is whether \(R(S)/\sqrt c\leq10^{-3}\). Two independently implemented exhaustive double-precision searches report no passing subset of size at most ten (13,432,735,555 subsets evaluated), and a passing eleven-channel witness \(S_{11}=\{0,1,3,42,43,44,45,46,47,48,49\}\). This remains a **numerical** statement until the error bounds below are certified.

## Uniform perturbation lemma

Suppose the computed coefficients \(\widehat c,\widehat f,\widehat Q\) obey certified bounds

\[
|c-\widehat c|\leq\epsilon_c,\qquad
\max_i|f_i-\widehat f_i|\leq\epsilon_f,\qquad
\max_{ij}|Q_{ij}-\widehat Q_{ij}|\leq\epsilon_Q.
\]

Suppose a verified exhaustive enumerator certifies that every subset of size at most ten has *computed-real-arithmetic* score \(\widehat R(S)^2\geq m\). Then every such subset satisfies

\[
R(S)^2-10^{-6}c\ \geq\ m-10^{-6}\widehat c
 -(1+10^{-6})\epsilon_c-10\epsilon_f-100\epsilon_Q.
\tag{1}
\]

This is immediate from the triangle inequality applied to the scalar, at most ten linear terms, and at most one hundred ordered Gram terms. There is no cancellation or distributional assumption in (1). If the enumerator itself uses floating arithmetic, subtract a **certified uniform scoring error** \(\epsilon_{\rm search}\) from its reported lower bound \(m\).

For a particular eleven-channel witness with computed score \(w\), the analogous sufficient condition for a true pass is

\[
10^{-6}\widehat c-w >(1+10^{-6})\epsilon_c+11\epsilon_f+121\epsilon_Q
 +\epsilon_{\rm witness}.
\tag{2}
\]

Here \(\epsilon_{\rm witness}\) covers any certified arithmetic error in computing \(w\).

## Size of the available margins

The archived direct reconstruction reports \(\widehat c=0.5045156715545931\), minimum ten-channel relative residual \(d_{10}=0.0010398206190990441\), and eleven-channel witness residual \(d_{11}=0.00096236912766441347\). The respective *squared-score* margins, using these rounded displayed values, are approximately

| Decision | Squared-score distance from the threshold |
|---|---:|
| Exclude all \(K\leq10\), contingent on the exhaustive minimum | \(4.0980254\times10^{-8}\) |
| Accept the specified \(K=11\) witness | \(3.7256294\times10^{-8}\) |

The author's search compares the direct residual with the Gram score to tolerance \(2\times10^{-12}\) in *relative residual*. Even taking that entire tolerance against the ten-channel margin leaves approximately \(4.09802519\times10^{-8}\). A convenient prospective proof target is

\[
\epsilon_c,\epsilon_f,\epsilon_Q\leq10^{-10},\qquad
\epsilon_{\rm search},\epsilon_{\rm witness}\leq10^{-9}.
\]

Equation (1) would then retain more than \(2.88\times10^{-8}\) of positive margin; (2) would retain more than \(2.29\times10^{-8}\). These are **required certification targets**, not error bounds already proved. The precise search lower bound should be captured directly from a rerun, rather than reconstructed from the rounded direct residual as done for this planning calculation.

As a diagnostic only, I rebuilt all 50 channels and 2,500 Gram entries with a separate extended-precision FFT (`scipy.fft`, 18-decimal-digit `longdouble` here). Its largest absolute discrepancies from the archived double coefficients were \(6.97\times10^{-15}\) for \(c\), \(1.35\times10^{-14}\) for \(f\), and \(6.94\times10^{-15}\) for \(Q\); the binary mask agreed exactly, with minimum observed stress-to-threshold distance \(0.0083468\). This corroborates ample numerical headroom but supplies **no outward-rounded interval enclosure**. The earlier independent 50-digit `mpmath` check covers the selected ten-channel optimum and eleven-channel witness only, not the full search.

## What would close this finite problem

1. Generate the 50 channel vectors and Gram coefficients with certified outward-rounded intervals, including the cosine/DFT evaluations and the mask decisions. Verify coefficient interval radii meet the bounds in (1) and (2).
2. Run or formally audit an exhaustive lexicographic or fixed-popcount search using exact rational scores for outward-rounded coefficient endpoints, or use a certified interval branch-and-bound. Record its minimum lower bound and the total count at each cardinality. A match to \(\binom{50}{K}\) alone does not prove coverage; the traversal invariant must also be checked.
3. Evaluate the specified eleven-channel witness with outward-rounded arithmetic and check its upper score against \(10^{-6}\) times a lower bound on \(c\).

Passing these steps would prove **\(K_{0.001}=11\) for this one fixed finite LRSC benchmark**. It would not imply the Navier–Stokes regularity conjecture or general LRSC bounds. No new computation should change the frozen v1.2 DOI release; any certificate should be a separately identified supplement.

## Source provenance

- `LRSC_v1_1_1_Source_Bundle.zip`: operator implementation, lexicographic search, and `VERIFICATION_OUTPUT.txt`.
- `LRSC_v1_1_1_Independent_Companion.zip`: distinct bitmask enumeration and two selected 50-digit checks.
- Frozen LRSC v1.2 DOI: `10.17605/OSF.IO/NM5BW`; the v1.1.1 numerical supplement is separately recorded as `10.17605/OSF.IO/JAK5X`.
