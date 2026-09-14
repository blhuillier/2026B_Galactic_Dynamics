"""Orbit integration utilities."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

__all__ = [
    "angular_momentum_z",
    "equatorial_circular_radius",
    "find_spherical_turning_points",
    "integrate_cartesian_orbit",
    "integrate_meridional_orbit",
    "leapfrog_orbit",
    "meridional_rhs",
    "spherical_acceleration",
    "spherical_specific_energy",
]

FloatArray = NDArray[np.floating]
AxisymmetricGradient = Callable[
    [ArrayLike, ArrayLike],
    tuple[FloatArray, FloatArray],
]

SphericalPotential = Callable[[ArrayLike], FloatArray]
SphericalRadialGradient = Callable[[ArrayLike], FloatArray]
CartesianAcceleration = Callable[[ArrayLike], FloatArray]


def meridional_rhs(
    _t: float,
    state: ArrayLike,
    *,
    gradient: AxisymmetricGradient,
    Lz: float,
) -> list[float]:
    """Return the meridional equations of motion at fixed Lz."""
    R, z, vR, vz = state

    if R <= 0.0:
        raise ValueError(
            "The cylindrical radius R must remain positive."
        )

    dphi_dR, dphi_dz = gradient(R, z)

    return [
        vR,
        vz,
        -dphi_dR + Lz**2 / R**3,
        -dphi_dz,
    ]
    
def integrate_meridional_orbit(
    initial_state: ArrayLike,
    t_eval: ArrayLike,
    *,
    gradient: AxisymmetricGradient,
    Lz: float,
    rtol: float = 1.0e-10,
    atol: float = 1.0e-12,
):
    """Integrate an orbit in the meridional plane at fixed Lz."""
    initial_state = np.asarray(initial_state, dtype=float)
    t_eval = np.asarray(t_eval, dtype=float)

    if initial_state.shape != (4,):
        raise ValueError(
            "initial_state must be [R, z, vR, vz]."
        )

    if initial_state[0] <= 0.0:
        raise ValueError(
            "The initial cylindrical radius R must be positive."
        )

    if t_eval.ndim != 1 or t_eval.size < 2:
        raise ValueError(
            "t_eval must contain at least two times."
        )

    if np.any(np.diff(t_eval) <= 0.0):
        raise ValueError(
            "t_eval must be strictly increasing."
        )

    solution = solve_ivp(
        lambda t, state: meridional_rhs(
            t,
            state,
            gradient=gradient,
            Lz=Lz,
        ),
        (t_eval[0], t_eval[-1]),
        initial_state,
        t_eval=t_eval,
        rtol=rtol,
        atol=atol,
    )

    if not solution.success:
        raise RuntimeError(
            f"Orbit integration failed: {solution.message}"
        )

    return solution
    
def equatorial_circular_radius(
    Lz: float,
    *,
    radial_gradient: Callable[[float], float],
    bracket: tuple[float, float],
) -> float:
    """Return the equatorial circular radius for a given Lz."""

    def circular_condition(R: float) -> float:
        return radial_gradient(R) - Lz**2 / R**3

    return brentq(
        circular_condition,
        *bracket,
    )
    
def spherical_acceleration(
    position: ArrayLike,
    *,
    radial_gradient: SphericalRadialGradient,
) -> FloatArray:
    """Return the Cartesian acceleration in a spherical potential."""
    position = np.asarray(position, dtype=float)

    radius = np.linalg.norm(position, axis=-1)

    if np.any(radius == 0.0):
        raise ValueError(
            "The Cartesian direction of the spherical force is "
            "undefined at r = 0."
        )

    dphi_dr = radial_gradient(radius)
    factor = -dphi_dr / radius

    return factor[..., np.newaxis] * position

def leapfrog_orbit(
    position0: ArrayLike,
    velocity0: ArrayLike,
    dt: float,
    n_steps: int,
    *,
    acceleration: CartesianAcceleration,
) -> tuple[FloatArray, FloatArray, FloatArray]:
    """Integrate an orbit with kick--drift--kick leapfrog."""
    position0 = np.asarray(position0, dtype=float)
    velocity0 = np.asarray(velocity0, dtype=float)

    if position0.ndim != 1:
        raise ValueError("position0 must be a one-dimensional vector.")

    if velocity0.shape != position0.shape:
        raise ValueError(
            "position0 and velocity0 must have the same shape."
        )

    if dt <= 0.0:
        raise ValueError("dt must be positive.")

    if n_steps < 1:
        raise ValueError("n_steps must be at least 1.")

    position = np.empty(
        (n_steps + 1, position0.size),
        dtype=float,
    )
    velocity = np.empty_like(position)

    position[0] = position0
    velocity[0] = velocity0

    for n in range(n_steps):
        acceleration_n = acceleration(position[n])

        velocity_half = (
            velocity[n]
            + 0.5 * dt * acceleration_n
        )

        position[n + 1] = (
            position[n]
            + dt * velocity_half
        )

        acceleration_np1 = acceleration(position[n + 1])

        velocity[n + 1] = (
            velocity_half
            + 0.5 * dt * acceleration_np1
        )

    time = dt * np.arange(n_steps + 1)

    return time, position, velocity

def spherical_specific_energy(
    position: ArrayLike,
    velocity: ArrayLike,
    *,
    potential: SphericalPotential,
) -> FloatArray:
    """Return the specific energy in a spherical potential."""
    position = np.asarray(position, dtype=float)
    velocity = np.asarray(velocity, dtype=float)

    radius = np.linalg.norm(position, axis=-1)
    speed_squared = np.sum(velocity**2, axis=-1)

    return 0.5 * speed_squared + potential(radius)

def angular_momentum_z(
    position: ArrayLike,
    velocity: ArrayLike,
) -> FloatArray:
    """Return the z-component of the specific angular momentum."""
    position = np.asarray(position, dtype=float)
    velocity = np.asarray(velocity, dtype=float)

    return (
        position[..., 0] * velocity[..., 1]
        - position[..., 1] * velocity[..., 0]
    )
    
def find_spherical_turning_points(
    
    energy: float,
    angular_momentum: float,
    *,
    potential: SphericalPotential,
    bracket: tuple[float, float],
    n_scan: int = 5000,
) -> tuple[float, float]:
    """Return the pericentre and apocentre of a non-circular bound orbit.
    
    The roots are identified through sign changes of
    E - Phi_eff(r). A circular orbit corresponds to a double root and is
    not handled by this routine.
    """
    r_min, r_max = bracket

    if r_min <= 0.0:
        raise ValueError("The lower radial bound must be positive.")

    radius_grid = np.geomspace(
        r_min,
        r_max,
        n_scan,
    )

    def radial_energy_difference(radius: ArrayLike) -> FloatArray:
        radius = np.asarray(radius, dtype=float)

        phi_eff = (
            potential(radius)
            + angular_momentum**2 / (2.0 * radius**2)
        )

        return energy - phi_eff

    values = radial_energy_difference(radius_grid)

    roots: list[float] = []

    for left, right, value_left, value_right in zip(
        radius_grid[:-1],
        radius_grid[1:],
        values[:-1],
        values[1:],
    ):
        if value_left == 0.0:
            roots.append(float(left))
        elif value_left * value_right < 0.0:
            root = brentq(
                radial_energy_difference,
                left,
                right,
            )
            roots.append(root)

    if len(roots) < 2:
        raise RuntimeError(
            "Could not locate both radial turning points."
        )

    return roots[0], roots[-1]

def integrate_cartesian_orbit(
    initial_state: ArrayLike,
    t_eval: ArrayLike,
    *,
    acceleration: CartesianAcceleration,
    rtol: float = 1.0e-10,
    atol: float = 1.0e-12,
):
    """Integrate a Cartesian orbit for a supplied acceleration law."""

    initial_state = np.asarray(initial_state, dtype=float)
    t_eval = np.asarray(t_eval, dtype=float)

    if initial_state.ndim != 1:
        raise ValueError("initial_state must be one-dimensional.")

    if initial_state.size == 0 or initial_state.size % 2 != 0:
        raise ValueError(
            "initial_state must contain equally sized position "
            "and velocity vectors."
        )

    if t_eval.ndim != 1 or t_eval.size < 2:
        raise ValueError("t_eval must contain at least two times.")

    if np.any(np.diff(t_eval) <= 0.0):
        raise ValueError("t_eval must be strictly increasing.")

    n_dim = initial_state.size // 2

    def rhs(_t, state):
        position = state[:n_dim]
        velocity = state[n_dim:]

        return np.concatenate(
            [
                velocity,
                acceleration(position),
            ]
        )

    solution = solve_ivp(
        rhs,
        (t_eval[0], t_eval[-1]),
        initial_state,
        t_eval=t_eval,
        rtol=rtol,
        atol=atol,
    )
    
    if not solution.success:
        raise RuntimeError(
            f"Orbit integration failed: {solution.message}"
        )

    return solution