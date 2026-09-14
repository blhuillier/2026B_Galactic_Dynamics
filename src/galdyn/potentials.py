"""Analytical gravitational potentials and density models."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray

FloatArray = NDArray[np.floating]


__all__ = [
    "kepler_dphi_dr",
    "kepler_potential",
    "kepler_d2phi_dr2",
    "axisymmetric_effective_potential",
    "logarithmic_dphi_dr",
    "logarithmic_potential",
    "logarithmic_d2phi_dr2",
    "miyamoto_nagai_gradient",
    "miyamoto_nagai_potential",
    "plummer_density",
    "plummer_dphi_dr",
    "plummer_enclosed_mass",
    "plummer_potential",
    "spherical_effective_potential",
    "harmonic_d2phi_dr2",
    "harmonic_dphi_dr",
    "harmonic_potential",
]

def _require_positive(value: float, name: str) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive.")
    
    
# Kepler Potential 

def kepler_potential(
    r: ArrayLike,
    *,
    G: float = 1.0,
    M: float = 1.0,
) -> FloatArray:
    """Return the Kepler potential."""
    r = np.asarray(r, dtype=float)

    if np.any(r <= 0.0):
        raise ValueError("r must be positive.")

    return -G * M / r


def kepler_dphi_dr(
    r: ArrayLike,
    *,
    G: float = 1.0,
    M: float = 1.0,
) -> FloatArray:
    """Return dPhi/dr for the Kepler potential."""
    r = np.asarray(r, dtype=float)

    if np.any(r <= 0.0):
        raise ValueError("r must be positive.")

    return G * M / r**2

def kepler_d2phi_dr2(
    r: ArrayLike,
    *,
    G: float = 1.0,
    M: float = 1.0,
) -> FloatArray:
    """Return d2Phi/dr2 for the Kepler potential."""
    r = np.asarray(r, dtype=float)

    if np.any(r <= 0.0):
        raise ValueError("r must be positive.")

    return -2.0 * G * M / r**3

# Plummer potential 

def plummer_potential(
    r: ArrayLike,
    *,
    G: float = 1.0,
    M: float = 1.0,
    b: float = 1.0,
) -> FloatArray:
    """Return the Plummer potential."""
    r = np.asarray(r, dtype=float)
    return -G * M / np.sqrt(r**2 + b**2)


def plummer_density(
    r: ArrayLike,
    *,
    M: float = 1.0,
    b: float = 1.0,
) -> FloatArray:
    """Return the Plummer density."""
    r = np.asarray(r, dtype=float)
    return (
        3.0 * M
        / (4.0 * np.pi * b**3)
        * (1.0 + r**2 / b**2) ** (-2.5)
    )


def plummer_enclosed_mass(
    r: ArrayLike,
    *,
    M: float = 1.0,
    b: float = 1.0,
) -> FloatArray:
    """Return the mass enclosed within radius r."""
    r = np.asarray(r, dtype=float)
    return M * r**3 / (r**2 + b**2) ** 1.5


def plummer_dphi_dr(
    r: ArrayLike,
    *,
    G: float = 1.0,
    M: float = 1.0,
    b: float = 1.0,
) -> FloatArray:
    """Return dPhi/dr for the Plummer potential."""
    r = np.asarray(r, dtype=float)
    return G * M * r / (r**2 + b**2) ** 1.5


# Miyamoto--Nagai potential
def miyamoto_nagai_potential(
    R: ArrayLike,
    z: ArrayLike,
    *,
    G: float = 1.0,
    M: float = 1.0,
    a: float = 1.0,
    b: float = 0.2,
) -> FloatArray:
    """Return the Miyamoto--Nagai potential."""
    R = np.asarray(R, dtype=float)
    z = np.asarray(z, dtype=float)

    zeta = np.sqrt(z**2 + b**2)
    return -G * M / np.sqrt(R**2 + (a + zeta) ** 2)


def miyamoto_nagai_gradient(
    R: ArrayLike,
    z: ArrayLike,
    *,
    G: float = 1.0,
    M: float = 1.0,
    a: float = 1.0,
    b: float = 0.2,
) -> tuple[FloatArray, FloatArray]:
    """Return dPhi/dR and dPhi/dz."""
    R = np.asarray(R, dtype=float)
    z = np.asarray(z, dtype=float)

    zeta = np.sqrt(z**2 + b**2)
    B = a + zeta
    denominator = (R**2 + B**2) ** 1.5

    dphi_dR = G * M * R / denominator
    dphi_dz = G * M * B * z / (zeta * denominator)

    return dphi_dR, dphi_dz

# Spherical Effective Potential

def spherical_effective_potential(
    r: ArrayLike,
    phi: ArrayLike,
    L: float,
) -> FloatArray:
    """Return Phi_eff = Phi + L^2 / (2r^2)."""
    r = np.asarray(r, dtype=float)
    phi = np.asarray(phi, dtype=float)
    return phi + L**2 / (2.0 * r**2)


def axisymmetric_effective_potential(
    R: ArrayLike,
    phi: ArrayLike,
    Lz: float,
) -> FloatArray:
    """Return Phi_eff = Phi + Lz^2 / (2R^2)."""
    R = np.asarray(R, dtype=float)
    phi = np.asarray(phi, dtype=float)
    return phi + Lz**2 / (2.0 * R**2)


# Logarithmic Potential

def logarithmic_potential(
    r: ArrayLike,
    *,
    v0: float = 1.0,
    rc: float = 0.4,
) -> FloatArray:
    """Return the spherical logarithmic potential."""
    r = np.asarray(r, dtype=float)
    return 0.5 * v0**2 * np.log(rc**2 + r**2)


def logarithmic_dphi_dr(
    r: ArrayLike,
    *,
    v0: float = 1.0,
    rc: float = 0.4,
) -> FloatArray:
    """Return dPhi/dr for the spherical logarithmic potential."""
    r = np.asarray(r, dtype=float)
    return v0**2 * r / (rc**2 + r**2)

def logarithmic_d2phi_dr2(
    r: ArrayLike,
    *,
    v0: float = 1.0,
    rc: float = 0.4,
) -> FloatArray:
    """Return d2Phi/dr2 for the spherical logarithmic potential."""
    r = np.asarray(r, dtype=float)

    denominator = (rc**2 + r**2) ** 2

    return (
        v0**2
        * (rc**2 - r**2)
        / denominator
    )

def harmonic_potential(
    r: ArrayLike,
    *,
    omega0: float = 1.0,
) -> FloatArray:
    """Return the spherical harmonic potential."""
    r = np.asarray(r, dtype=float)
    return 0.5 * omega0**2 * r**2


def harmonic_dphi_dr(
    r: ArrayLike,
    *,
    omega0: float = 1.0,
) -> FloatArray:
    """Return dPhi/dr for the spherical harmonic potential."""
    r = np.asarray(r, dtype=float)
    return omega0**2 * r


def harmonic_d2phi_dr2(
    r: ArrayLike,
    *,
    omega0: float = 1.0,
) -> FloatArray:
    """Return d2Phi/dr2 for the spherical harmonic potential."""
    r = np.asarray(r, dtype=float)
    return np.full_like(
        r,
        omega0**2,
        dtype=float,
    )