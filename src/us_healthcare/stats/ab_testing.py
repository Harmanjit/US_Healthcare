from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class TwoProportionResult:
    p_a: float
    p_b: float
    diff: float
    z: float
    p_value_approx: float


def two_proportion_z_test(
    success_a: int,
    n_a: int,
    success_b: int,
    n_b: int,
) -> TwoProportionResult:
    """
    Two-proportion z-test with a normal approximation.

    This is intentionally dependency-light (no scipy), suitable as a starting point.
    For serious work, you may want Fisher's exact test or a bootstrap CI.
    """
    if n_a <= 0 or n_b <= 0:
        raise ValueError("n_a and n_b must be > 0")
    if not (0 <= success_a <= n_a and 0 <= success_b <= n_b):
        raise ValueError("successes must be within [0, n]")

    p_a = success_a / n_a
    p_b = success_b / n_b
    p_pool = (success_a + success_b) / (n_a + n_b)
    se = np.sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b))
    if se == 0:
        return TwoProportionResult(p_a, p_b, p_b - p_a, z=float("nan"), p_value_approx=float("nan"))

    z = (p_b - p_a) / se
    # Two-sided p-value approximation via normal CDF using erf.
    p = 2 * (1 - _phi(abs(z)))
    return TwoProportionResult(p_a=p_a, p_b=p_b, diff=p_b - p_a, z=float(z), p_value_approx=float(p))


def _phi(x: float) -> float:
    # Standard normal CDF approximation using erf
    return 0.5 * (1.0 + float(np.math.erf(x / np.sqrt(2.0))))

