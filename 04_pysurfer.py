"""Load and render the inflated surface with PySurfer (Mayavi/VTK).

PySurfer is the classic Python tool for surface visualization. Its ``Brain``
object loads surfaces from a FreeSurfer ``SUBJECTS_DIR`` layout, so we first
materialize our canonical GIFTI asset (``data/*.inflated.gii.gz``) into a
minimal ``fsaverage`` subject directory -- keeping the *same* geometry every
other example uses -- then hand it to PySurfer.

## Why this one needs conda

PySurfer depends on Mayavi, whose ``tvtk`` build does not compile against the
VTK wheels available for Python 3.12+. The reliable environment is conda-forge:

    conda env create -f environment-pysurfer.yml
    conda activate surface-pysurfer
    python 04_pysurfer.py

(See ``environment-pysurfer.yml``. Verified with Python 3.11, mayavi 4.8.3,
pysurfer 0.11.2, vtk 9.4.2, numpy 1.26.)

## Rendering note

macOS VTK has no OSMesa, so we render in an on-screen OpenGL window (works in a
desktop session) rather than truly offscreen. On headless Linux, wrap the call
in ``xvfb-run`` and set ``mlab.options.offscreen = True``.
"""

from __future__ import annotations

import os

# Must be set before importing mayavi: pick one Qt binding to avoid Qt5/Qt6
# symbol clashes in the conda env.
os.environ.setdefault("QT_API", "pyqt5")
os.environ.setdefault("ETS_TOOLKIT", "qt")

from pathlib import Path

import nibabel as nib
import numpy as np

REPO = Path(__file__).parent
DATA = REPO / "data"
OUT = REPO / "outputs"
SUBJECTS_DIR = DATA / "subjects"


def build_fsaverage_subject() -> None:
    """Convert the canonical GIFTI surfaces into a minimal SUBJECTS_DIR.

    Writes ``fsaverage/surf/{lh,rh}.inflated`` (FreeSurfer binary geometry) and
    a flat ``{lh,rh}.curv`` so PySurfer's default curvature shading has data.
    """
    surf = SUBJECTS_DIR / "fsaverage" / "surf"
    surf.mkdir(parents=True, exist_ok=True)

    for hemi, fsh in (("left", "lh"), ("right", "rh")):
        src = DATA / f"{hemi}.inflated.gii.gz"
        if not src.exists():
            raise SystemExit("Run 00_fetch_surface.py first to populate data/.")
        gii = nib.load(str(src))
        coords = np.asarray(gii.agg_data("NIFTI_INTENT_POINTSET"))
        faces = np.asarray(gii.agg_data("NIFTI_INTENT_TRIANGLE"))
        nib.freesurfer.write_geometry(str(surf / f"{fsh}.inflated"), coords, faces)
        nib.freesurfer.write_morph_data(
            str(surf / f"{fsh}.curv"), np.zeros(coords.shape[0], dtype="float32")
        )


def main() -> None:
    OUT.mkdir(exist_ok=True)
    build_fsaverage_subject()
    os.environ["SUBJECTS_DIR"] = str(SUBJECTS_DIR)

    from mayavi import mlab

    # On-screen rendering (see module docstring for the headless-Linux variant).
    mlab.options.offscreen = False

    from surfer import Brain

    brain = Brain(
        "fsaverage", "lh", "inflated",
        subjects_dir=str(SUBJECTS_DIR),
        background="white",
        views=["lateral"],
    )
    print("pysurfer: rendered fsaverage5 left inflated (10242 verts)")

    out = OUT / "04_pysurfer.png"
    brain.save_image(str(out))
    brain.close()
    print("wrote", out)


if __name__ == "__main__":
    main()
