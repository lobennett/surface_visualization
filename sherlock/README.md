# surface_visualization on Sherlock

A Sherlock-ready notebook port of the [`surface_visualization`](../README.md)
demos, plus **"plug into your pipeline"** cells that overlay your own surface
data (e.g. CBIG/MSHBM `fsaverage6` outputs) on the canonical inflated surface.

- **`surface_visualization_sherlock.ipynb`** — the notebook. Demos 00–03 run
  interactively; 04 (PySurfer) renders headless via a batch job; 05/06
  (FreeSurfer/MATLAB) are Sherlock module recipes.

Everything writes to `$SCRATCH` (never `$HOME`), renders headless, and runs on a
compute node — per the Sherlock house rules.

---

## 1. Build the kernel (once)

`nilearn`/`nibabel`/`plotly` aren't Lmod modules, so put them in a `uv` venv on
`$SCRATCH` and register it as a Jupyter kernel. **Do this on a compute node, not
the login node** (`uv pip install` is real work):

```bash
sh_dev                                   # interactive compute node
module load uv/0.9.5
uv venv $SCRATCH/surface-viz-venv --python 3.12
source $SCRATCH/surface-viz-venv/bin/activate
uv pip install nilearn nibabel plotly matplotlib numpy ipykernel
python -m ipykernel install --user --name surface-viz --display-name "surface-viz"
```

This registers `~/.local/share/jupyter/kernels/surface-viz` (tiny JSON — fine on
`$HOME`). The venv itself lives on `$SCRATCH`.

> **`$SCRATCH` is purged after 90 days of inactivity** and is not backed up. If
> the venv disappears, just re-run the block above. For something longer-lived,
> put the venv on `$GROUP_HOME` instead.

---

## 2. Launch Jupyter — pick one

### A. Sherlock OnDemand (easiest)

1. Go to <https://ondemand.sherlock.stanford.edu> → **Interactive Apps →
   Jupyter**.
2. Request a session (e.g. partition `normal`, 2 cores, 8 GB, 2 h).
3. Open it, then choose the **surface-viz** kernel (top-right) for this notebook.

### B. `sh_dev` + SSH port-forward (CLI)

```bash
# on Sherlock:
sh_dev
source $SCRATCH/surface-viz-venv/bin/activate
jupyter lab --no-browser --port 8888 --ip 0.0.0.0   # note the node name, e.g. sh03-01

# on your laptop (replace sh03-01 with the node printed above):
ssh -L 8888:sh03-01:8888 <sunetid>@login.sherlock.stanford.edu
# then open the printed http://127.0.0.1:8888/?token=... URL
```

### C. Headless / batch (for pipeline integration)

Run the whole notebook unattended in a Slurm job — no display, outputs land in
`$SCRATCH/surface_viz_work/outputs/`:

```bash
cat > render.sbatch <<'EOF'
#!/bin/bash
#SBATCH -p normal
#SBATCH --time=00:30:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=8GB
source $SCRATCH/surface-viz-venv/bin/activate
jupyter nbconvert --to notebook --execute --inplace \
    $SCRATCH/surface_visualization/sherlock/surface_visualization_sherlock.ipynb
EOF
sbatch render.sbatch
```

For per-subject parameterization, install `papermill` into the venv and pass
parameters instead.

---

## 3. PySurfer (demo 04) — separate conda env

PySurfer needs Mayavi/VTK + OpenGL, which don't fit the `uv` venv. Demo 04's
cell writes a conda env file, a headless render script, and an sbatch wrapper to
`$SCRATCH/surface_viz_work/`. Then:

```bash
# install conda on $GROUP_HOME (not $HOME) if you don't have it, then:
conda env create -f $SCRATCH/surface_viz_work/environment-pysurfer.yml
sbatch $SCRATCH/surface_viz_work/04_pysurfer.sbatch     # uses xvfb-run + offscreen
```

---

## 4. What the demos do

Each runnable demo (01–03) loads the same nilearn-fetched `fsaverage5` surface,
renders it inline, and saves the result to `$SCRATCH/surface_viz_work/outputs/`:

- `01_nilearn.png` — nilearn `plot_surf`
- `02_nibabel.png` — raw `(coords, faces)` via nibabel + matplotlib trisurf
- `03_plotly.html` — interactive 3D mesh (rotate/zoom)
- `04_pysurfer.png` — from the conda + xvfb batch job

To adapt for your own pipeline, point the load step at your surface file instead
of the fetched one and (optionally) pass a per-vertex vector — `plot_surf` takes
`surf_map=`, Plotly takes `intensity=`. The demos here keep it to the canonical
nilearn surface.

---

## Sherlock gotchas baked in

| Concern | Handling |
|---|---|
| `$HOME` is small (15 GB, NFS) | caches (`XDG_CACHE_HOME`, `MPLCONFIGDIR`, `NILEARN_DATA`) + all I/O → `$SCRATCH` |
| No display on compute nodes | matplotlib `Agg`, Plotly inline/HTML, PySurfer `xvfb` + `offscreen` |
| Login node is shared | installs/renders on `sh_dev`/OnDemand/sbatch, never the login node |
| Compute-node internet via proxy | fetch (demo 00) caches to `$SCRATCH`; run once on login/DTN or set `https_proxy` |
| Never guess module versions | `ml spider freesurfer` / `ml spider matlab` before loading |
