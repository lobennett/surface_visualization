"""Load the inflated surface at the lowest level with nibabel.

nibabel is the foundation most other tools build on. It reads both:

  * FreeSurfer binary geometry  (e.g. ``lh.inflated``) via ``read_geometry``
  * GIFTI surface files         (e.g. ``*.surf.gii``)   via ``nib.load``

Our canonical asset is GIFTI (``data/left.inflated.gii.gz``), so we demonstrate
the GIFTI path and explain the FreeSurfer path. Either way you get back two
NumPy arrays: vertex coordinates and triangle faces.

    python 02_nibabel.py  (run 00_fetch_surface.py first)
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np

DATA = Path(__file__).parent / "data"
OUT = Path(__file__).parent / "outputs"


def load_gifti_surface(path: Path) -> tuple[np.ndarray, np.ndarray]:
    """Return (coords, faces) from a GIFTI surface file."""
    gii = nib.load(str(path))
    # A surface GIFTI stores a POINTSET array (coords) and a TRIANGLE array.
    coords = gii.agg_data("NIFTI_INTENT_POINTSET")
    faces = gii.agg_data("NIFTI_INTENT_TRIANGLE")
    return np.asarray(coords), np.asarray(faces)


def main() -> None:
    OUT.mkdir(exist_ok=True)

    path = DATA / "left.inflated.gii.gz"
    if not path.exists():
        raise SystemExit("Run 00_fetch_surface.py first to populate data/.")

    coords, faces = load_gifti_surface(path)
    print(f"nibabel (GIFTI): {coords.shape[0]} vertices, {faces.shape[0]} faces")
    print(f"  coords dtype={coords.dtype}, bounds x[{coords[:,0].min():.1f}, "
          f"{coords[:,0].max():.1f}]")

    # For a FreeSurfer binary surface instead, the call is:
    #
    #     coords, faces = nib.freesurfer.read_geometry("lh.inflated")
    #
    # which returns the same (coords, faces) shapes.

    # Render the raw mesh with matplotlib's 3D triangulation to prove the
    # arrays are usable without any specialised plotting library.
    fig = plt.figure(figsize=(6, 5))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_trisurf(
        coords[:, 0], coords[:, 1], faces, coords[:, 2],
        cmap="bone", linewidth=0, antialiased=False,
    )
    ax.set_title("fsaverage5 inflated (nibabel + matplotlib trisurf)")
    ax.set_axis_off()
    ax.view_init(elev=10, azim=-90)
    out = OUT / "02_nibabel.png"
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print("wrote", out)


if __name__ == "__main__":
    main()
