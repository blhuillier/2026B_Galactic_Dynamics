# Galactic Dynamics — Student Exercises

Exercise notebooks accompanying the Master's-level course **Stellar Dynamics and Gravitation**.

This repository contains:

- Jupyter notebooks for students to explore the concepts introduced in lecture, test limiting cases, and run numerical experiments;
- `galdyn`, a small Python toolkit implementing the analytical potentials and orbit integrators used throughout the course.

The notebooks are meant to be played with: change parameters, break things, and see what happens. Most sections end with open-ended exercises rather than a fixed set of answers.

## Course outline

1. **Galaxies as Dynamical Systems**  
   Characteristic scales, crossing and relaxation times, the continuum limit, distribution functions, and the self-consistency problem.

2. **Newtonian Gravitation and Potential Theory**  
   Gravitational fields and potentials, Poisson's equation, Green's functions, shell theorems, and potential–density pairs.

3. **Orbits in Spherical Potentials**  
   Conserved quantities, effective potentials, turning points, circular orbits, radial motion, and apsidal precession.

4. **Orbits in Axisymmetric Potentials**  
   Meridional motion, circular frequencies, epicyclic motion, guiding centres, rotation curves, and Oort constants.

5. **Rotating and Non-Axisymmetric Potentials**  
   Rotating frames, the Jacobi integral, zero-velocity curves, barred potentials, resonances, and surfaces of section.

6. **Actions, Angles, and Resonances**  
   Action–angle variables, invariant tori, resonant dynamics, the pendulum approximation, phase mixing, and stream formation.

7. **Phase-Space Dynamics**  
   The collisionless Boltzmann equation, Liouville's theorem, characteristics, phase mixing, and coarse graining.

8. **Equilibrium Distribution Functions**  
   Jeans' theorem, ergodic and anisotropic distribution functions, Eddington inversion, and phase-space consistency.

9. **Jeans Equations and the Virial Theorem**  
   Velocity moments, spherical and axisymmetric Jeans equations, mass estimators, anisotropy, and the tensor virial theorem.

10. **Stellar Disks**  
    Thin-disk dynamics, vertical equilibrium, epicyclic motion, disk distribution functions, and local kinematics.

11. **Stability and Collective Phenomena**  
    Linear perturbations, Jeans instability, disk stability, the Toomre criterion, and collective gravitational response.

12. **Spiral Structure and Bars**  
    Density waves, swing amplification, spiral resonances, bar-supporting orbit families, and secular angular-momentum transport.

13. **Encounters, Relaxation, and Dynamical Friction**  
    Two-body encounters, relaxation, diffusion in velocity space, mass segregation, and Chandrasekhar dynamical friction.

14. **Tides, Streams, and Galactic Evolution**  
    Tidal radii, stripping, tidal streams, satellite disruption, mergers, and secular evolution.

## Exercise notebooks

Notebooks are added over the course of the semester as chapters are covered:

- [Chapter 1 — Galaxies as Dynamical Systems](notebooks/chapter_01/)
- [Chapter 2 — Newtonian Gravitation and Potential Theory](notebooks/chapter_02/)

## The `galdyn` toolkit

`galdyn` is deliberately small. Its functions are direct translations of the formulas developed in lecture — `plummer_dphi_dr`, `kepler_d2phi_dr2`, and so on read like the equations they implement, rather than hiding them behind a general-purpose framework. That is the point: you should be able to open `src/galdyn/potentials.py` and see exactly what each notebook is calling.

For later chapters (orbit integration in realistic potentials, actions and angles), we will introduce [`galpy`](https://docs.galpy.org/), the field-standard package for galactic dynamics, once the underlying concepts have been built by hand.

## Running the notebooks with uv

The recommended way to manage the Python environment is with **uv**, a fast, single-binary Python package and project manager. You do not need Python pre-installed — uv can fetch it for you.

### Installing uv

**macOS / Linux** — open a terminal and run:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows** — open PowerShell and run:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

If you already have Python and pip/pipx set up, `pip install uv` or `pipx install uv` also works.

Check the install with:

```bash
uv --version
```

(You may need to restart your terminal first so `uv` is on your `PATH`.)

### Setting up the environment

Clone the repository:

```bash
git clone https://github.com/blhuillier/2026B_Galactic_Dynamics.git
cd 2026B_Galactic_Dynamics
```

Create a virtual environment (any Python ≥ 3.11 works; uv will pick up whatever you have installed, or pass `--python 3.x` to request a specific version, downloading it if needed):

```bash
uv venv .venv --prompt GalDyn
```

Activate it:

```bash
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\activate         # Windows (Command Prompt)
.venv\Scripts\Activate.ps1     # Windows (PowerShell)
```

Your shell prompt should now show `(GalDyn)`. Install the project's dependencies and launch Jupyter Lab:

```bash
uv sync
uv run jupyter lab
```

Once Jupyter Lab is open, navigate to the relevant chapter directory under `notebooks/` and open the notebook.

## Licence

Unless stated otherwise, the code and notebooks in this repository are released under the [MIT License](LICENSE).

This repository does not include the lecture notes themselves; it accompanies them.

## Author

Benjamin L'Huillier  
Department of Physics and Astronomy  
Sejong University
