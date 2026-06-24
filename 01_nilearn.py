"""Load and render the inflated surface with nilearn.

nilearn is the canonical modern Python approach for surface plotting. It can
fetch standard meshes directly and render them with a single call.

We render a static view to PNG with the matplotlib engine (headless via the
``Agg`` backend). nilearn also offers ``view_surf`` for an interactive
HTML/JS view -- see the commented block below.

    python 01_nilearn.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless; no display required
import matplotlib.pyplot as plt

from nilearn.datasets import load_fsaverage
from nilearn.plotting import plot_surf

OUT = Path(__file__).parent / "outputs"


def main() -> None:
    OUT.mkdir(exist_ok=True)

    # nilearn can hand us the fsaverage surface directly -- no manual file paths.
    fsaverage = load_fsaverage(mesh="fsaverage5")
    inflated = fsaverage["inflated"]
    left = inflated.parts["left"]

    print(f"nilearn: left hemi has {left.n_vertices} vertices, "
          f"{left.faces.shape[0]} faces")

    # plot_surf accepts the PolyMesh (or a single hemisphere mesh) and returns
    # a matplotlib figure when engine="matplotlib".
    fig = plot_surf(
        left,
        hemi="left",
        view="lateral",
        engine="matplotlib",
        title="fsaverage5 inflated (nilearn)",
    )
    out = OUT / "01_nilearn.png"
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print("wrote", out)

    # Interactive alternative (writes a self-contained HTML you can open):
    #
    #     from nilearn.plotting import view_surf
    #     view = view_surf(left)
    #     view.save_as_html(OUT / "01_nilearn_interactive.html")


if __name__ == "__main__":
    main()
