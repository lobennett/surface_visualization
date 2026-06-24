"""Fetch the canonical inflated cortical surface used by every example.

We use nilearn to fetch the ``fsaverage`` surface. nilearn caches the data and
returns a ``FileMesh`` whose ``file_path`` points at a standard-format GIFTI
file. We copy that file into ``data/`` so the other scripts -- and the
documented FreeSurfer / MATLAB snippets -- can all point at the *same* canonical
asset.

We use ``fsaverage5`` (~10k vertices per hemisphere): the canonical lightweight
standard mesh.

Run this first:

    python 00_fetch_surface.py
"""

from __future__ import annotations

import shutil
from pathlib import Path

from nilearn.datasets import load_fsaverage

DATA_DIR = Path(__file__).parent / "data"


def fetch() -> dict[str, Path]:
    """Fetch fsaverage5 and copy each inflated hemisphere into ``data/``.

    Returns a mapping ``{"left": path, "right": path}``.
    """
    DATA_DIR.mkdir(exist_ok=True)

    fsaverage = load_fsaverage(mesh="fsaverage5")
    inflated = fsaverage["inflated"]  # PolyMesh with .parts["left"|"right"]

    paths: dict[str, Path] = {}
    for hemi in ("left", "right"):
        mesh = inflated.parts[hemi]
        src = Path(mesh.file_path)
        # Preserve the original suffix (e.g. ".gii.gz") so downstream tools can
        # detect the format from the filename.
        suffix = "".join(src.suffixes)  # e.g. ".gii.gz"
        dst = DATA_DIR / f"{hemi}.inflated{suffix}"
        shutil.copy(src, dst)
        paths[hemi] = dst
    return paths


def main() -> None:
    paths = fetch()
    print("Canonical inflated surface ready in", DATA_DIR)
    for hemi, dst in paths.items():
        print(f"  {hemi:5s} -> {dst.name}")


if __name__ == "__main__":
    main()
