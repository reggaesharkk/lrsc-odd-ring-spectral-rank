# Exact amplitude and threshold region for the fixed LRSC certificate

At fixed \(M=99\) and \(k_{\rm idx}=49\), the
[certificate](k001-certificate/CERTIFICATE.md) at \((A,\theta)=(0.5,0.08)\)
extends to a two-parameter region. In particular,

- at \(\theta=0.08\), \(K_{0.001}=11\) for every
  \(A\in[0.475795,0.529975]\);
- on the closed rectangle
  \(A\in[0.49,0.51]\), \(\theta\in[0.074084,0.084848]\),
  \(K_{0.001}=11\).

The full sufficient region is larger. Let \(s_-=7120634332350612482423087694352362/10^{35}\)
be the certified upper bound for the greatest baseline stress at an inactive
site, and \(s_+=8834680737317693635577446867804288/10^{35}\) the certified
lower bound for the least baseline stress at an active site. For any \(A>0\),

\[
4A^2s_-\leq\theta<4A^2s_+ \tag{1}
\]

is sufficient to keep exactly the same 81 active and 18 inactive sites as at
\((A,\theta)=(0.5,0.08)\). The inclusivity of the lower inequality follows
from the strict mask definition \(m_i=\mathbf1[C_i>\theta]\).

To see why, put \(c_i=\cos(2\pi 49i/99)\). For positive \(A\),
\(X_i(A)=1+Ac_i\), and hence

\[
C_i(A)=4A^2C_i(0.5),\qquad
j_i(A)=A\bigl(c_i-\min(c_{i-1},c_i,c_{i+1})\bigr).
\]

Condition (1) leaves the mask unchanged. Consequently the target spectrum
and every one of the 50 channel vectors are multiplied by the same positive
factor \(A/0.5\) relative to the baseline. Every normalized subset residual
is exactly constant throughout (1), so the existing exhaustive lower bound
and eleven-channel witness apply without a new subset search.

The [checker](amplitude_region.py) evaluates the interval endpoints and the
rectangle corners with exact rational arithmetic using the baseline stress
enclosures. Run `python3 finite-benchmark/amplitude_region.py` from the
repository root. No conclusion here extends to a different mode index,
ring size, or a parameter point where the mask changes.
