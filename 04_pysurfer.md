# PySurfer (documented)

[PySurfer](https://pysurfer.github.io/) is the classic Python tool for surface
visualization, built on **Mayavi** (VTK). It produces publication-quality 3D
renderings and is tightly integrated with the FreeSurfer `SUBJECTS_DIR` layout.

> **Why documented and not runnable here:** PySurfer depends on `mayavi`, which
> needs a working VTK + GUI/OpenGL toolchain and does not install cleanly on
> recent Python (3.12+). For a fully-runnable interactive 3D mesh, see
> [`03_plotly.py`](03_plotly.py).

## Install

```bash
pip install pysurfer mayavi
# Linux headless rendering also needs e.g.:  apt-get install xvfb
```

## Load an inflated surface

PySurfer's `Brain` object loads a subject's surface directly from
`SUBJECTS_DIR` by name — you give it the subject, hemisphere, and surface type
(`inflated`):

```python
import os
from surfer import Brain

# Point at a FreeSurfer subjects directory containing `fsaverage`.
os.environ["SUBJECTS_DIR"] = os.environ.get(
    "SUBJECTS_DIR", "/path/to/freesurfer/subjects"
)

brain = Brain(
    subject_id="fsaverage",
    hemi="lh",
    surf="inflated",          # <- the inflated geometry
    background="white",
)

# Save a static snapshot.
brain.save_image("04_pysurfer.png")
```

## Load from an explicit mesh instead

If you already have vertices/faces (e.g. loaded with nibabel from this repo's
`data/`), you can hand them to Mayavi directly:

```python
import nibabel as nib
from mayavi import mlab

gii = nib.load("data/left.inflated.gii.gz")
coords = gii.agg_data("NIFTI_INTENT_POINTSET")
faces = gii.agg_data("NIFTI_INTENT_TRIANGLE")

mlab.triangular_mesh(
    coords[:, 0], coords[:, 1], coords[:, 2], faces, color=(0.8, 0.8, 0.8)
)
mlab.savefig("04_pysurfer_mesh.png")
```

## Expected output

A smooth, shaded 3D inflated left hemisphere (lateral view) — visually
equivalent to the nilearn and Plotly renders in [`outputs/`](outputs/), with
Mayavi's characteristic lighting.
