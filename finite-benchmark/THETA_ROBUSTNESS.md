# A certified threshold plateau for the fixed LRSC benchmark

The [exact-integer certificate](k001-certificate/CERTIFICATE.md) establishes
\(K_{0.001}=11\) at \(M=99\), \(k_{\rm idx}=49\), \(A=1/2\), and \(\theta=0.08\).
The same conclusion holds for **every real threshold**

\[
\boxed{0.071206344\leq\theta\leq0.088346807.}
\]

This is an exact stability statement about the fixed operator, not a sampled
parameter sweep. Write
\(C_i=\tfrac12[(X_i-X_{i-1})^2+(X_i-X_{i+1})^2]\) and
\(m_i(\theta)=\mathbf1[C_i>\theta]\). At fixed \(M,k_{\rm idx},A\), the
state \(X\), stress \(C\), and redistribution \(j\) are independent of
\(\theta\). The integer interval construction bounds the greatest stress
among the 18 inactive sites from above by

\[
\max_{m_i(0.08)=0} C_i
\leq \frac{7120634332350612482423087694352362}{10^{35}}
<0.071206344,
\]

and the least stress among the 81 active sites from below by

\[
\min_{m_i(0.08)=1} C_i
\geq \frac{8834680737317693635577446867804288}{10^{35}}
>0.088346807.
\]

Thus every mask bit is unchanged throughout the stated *closed* interval.
The target, each of the 50 channels, their Gram objective, and every subset
residual are therefore exactly the same objects certified at \(\theta=0.08\).
Consequently the previously certified minimum passing cardinality remains 11
throughout this threshold interval.

Reproduce the two integer comparisons with
`python3 finite-benchmark/theta_robustness.py` from the repository root. The
claim holds only at the fixed \(M=99,k_{\rm idx}=49,A=1/2\); varying amplitude
or mode index requires a separate argument.
