# Experiments

## 001 — Partial prime-prefix recovery

**Question:** Can a balanced toy RSA modulus be factored when the high bits of one
prime are known and only a small low-bit suffix is unknown?

Let the hidden prime be

\[
p = p_0 + x, \qquad 0 \le x < X=2^r,
\]

where `p0` is the disclosed high-bit prefix shifted back into position and `r`
is the number of unknown low bits. Because `p` divides `N=pq`,

\[
f(x)=p_0+x \equiv 0 \pmod p.
\]

This is an **unknown-divisor** small-root problem. For a balanced RSA modulus,
`p` is approximately `N^(1/2)`, so the unknown-divisor parameter is approximately
`beta=1/2`. For a monic linear polynomial, the indicative Coppersmith bound is
`X < N^(beta^2-epsilon)`, i.e. roughly `N^(1/4-epsilon)`. The exact theorem
conditions and implementation parameters matter; the exponent is not a promise
for every finite instance.

Run from the project root with SageMath:

```bash
sage experiments/001_partial_prime_prefix.sage
```

The script writes `results/experiment_001.json`. It verifies any recovered
candidate by exact divisibility. The true factors are included in the JSON only
as toy-experiment ground truth, not as attack input.

**Scope:** This is a reproducible educational demonstration on tiny, generated
parameters. It is not a practical attack on correctly generated RSA keys, and
it must not be used against real systems or private keys.
