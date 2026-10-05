# Galactic Dynamics — Student Exercises

Exercise notebooks accompanying the Master's-level course **Stellar Dynamics and Gravitation**.

This repository contains:

- Jupyter notebooks for students to explore the concepts introduced in lecture, test limiting cases, and run numerical experiments;
- `galdyn`, a small Python toolkit implementing the analytical potentials and orbit integrators used throughout the course.

The notebooks are meant to be played with: change parameters, break things, and see what happens. Most sections end with open-ended exercises rather than a fixed set of answers.

## Course outline

Chapter numbering follows the lecture notes.

### Part I — Gravitational and Dynamical Foundations

1. **Galaxies as Dynamical Systems**  
   Galactic components, characteristic scales, dynamical timescales, and the distinction between collisionless and collisional systems.

2. **Newtonian Gravitation and Potential Theory**  
   Poisson's equation, Green's functions, spherical and axisymmetric systems, multipole expansions, and common galactic models.

3. **Elements of Classical Mechanics**  
   Lagrangian and Hamiltonian mechanics, Poisson brackets, integrals of motion, canonical transformations, integrable motion, and action–angle variables.

### Part II — Spherical and Collisionless Stellar Systems

4. **Orbits in Spherical Potentials**  
   Effective potentials, circular orbits, orbital frequencies, apsidal precession, actions and angles, and numerical orbit integration.

5. **Phase-Space Dynamics and Collisionless Equilibria**  
   Distribution functions, Liouville's theorem, the collisionless Boltzmann equation, Jeans' theorem, phase mixing, and violent relaxation.

6. **Spherical Distribution Functions and Mass Modelling**  
   Eddington inversion, velocity moments and anisotropy, the spherical Jeans equation, projected observables, the mass–anisotropy degeneracy, and the virial theorem.

### Part III — Galactic Disks

7. **Gravitation, Rotation, and Kinematics of Galactic Disks**  
   Thin-disk gravity, exponential disks, flattened potential–density pairs, rotation curves, and local galactic rotation.

8. **Orbits in Axisymmetric Potentials**  
   Meridional motion, circular orbits and guiding centres, the epicyclic approximation, the third integral, and actions in axisymmetric potentials.

9. **Equilibrium Stellar Disks**  
   Disk distribution functions, cold and warm disks, Jeans equations in cylindrical coordinates, asymmetric drift, and vertical equilibrium.

10. **Stability and Collective Phenomena**  
    Local axisymmetric stability, the relation to Jeans instability, waves in stellar disks, swing amplification, and bending instabilities.

### Part IV — Non-Axisymmetry and Galactic Evolution

11. **Spiral Structure and Bars**  
    Rotating reference frames, the Jacobi integral, corotation and Lindblad resonances, bar-supporting orbit families, and angular-momentum exchange with a pattern.

12. **Resonant and Chaotic Dynamics**  
    Perturbations in action–angle variables, resonant trapping, separatrices and resonance overlap, surfaces of section, chaos diagnostics, and adiabatic invariance.

13. **Encounters, Relaxation, and Dynamical Friction**  
    Two-body encounters, diffusion in velocity space, the relaxation time, mass segregation, evaporation, and dynamical friction.

14. **Tides, Streams, and Galactic Evolution**  
    Tidal fields, the Hill approximation and tidal radius, tidal shocks, satellite disruption, stellar streams as probes of the potential, mergers, and secular evolution.
## Exercise notebooks

Notebooks are added over the course of the semester as chapters are covered:

- [Chapter 1 — Galaxies as Dynamical Systems](notebooks/chapter_01/)
- [Chapter 2 — Newtonian Gravitation and Potential Theory](notebooks/chapter_02/)
- [Chapter 3 — Elements of Classical Mechanics](notebooks/chapter_03/)
- [Chapter 4 — Orbits in Spherical Potentials](notebooks/chapter_04/)

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
