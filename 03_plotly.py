"""Render the inflated surface as an interactive 3D mesh with Plotly.

Plotly produces a self-contained HTML file you can open in any browser and
rotate / zoom -- with no OpenGL, display server, or native dependencies. That
makes it a reliable, fully runnable stand-in for heavier interactive engines
(PySurfer/mayavi, pyvista), which are covered as documented examples.

We also export a static PNG (via kaleido) so the README can embed a preview.

    python 03_plotly.py  (run 00_fetch_surface.py first)
"""

from __future__ import annotations

from pathlib import Path

import nibabel as nib
import numpy as np
import plotly.graph_objects as go

DATA = Path(__file__).parent / "data"
OUT = Path(__file__).parent / "outputs"


def load_gifti_surface(path: Path) -> tuple[np.ndarray, np.ndarray]:
    gii = nib.load(str(path))
    coords = np.asarray(gii.agg_data("NIFTI_INTENT_POINTSET"))
    faces = np.asarray(gii.agg_data("NIFTI_INTENT_TRIANGLE"))
    return coords, faces


def main() -> None:
    OUT.mkdir(exist_ok=True)

    path = DATA / "left.inflated.gii.gz"
    if not path.exists():
        raise SystemExit("Run 00_fetch_surface.py first to populate data/.")

    coords, faces = load_gifti_surface(path)
    print(f"plotly: {coords.shape[0]} vertices, {faces.shape[0]} faces")

    mesh = go.Mesh3d(
        x=coords[:, 0], y=coords[:, 1], z=coords[:, 2],
        i=faces[:, 0], j=faces[:, 1], k=faces[:, 2],
        color="lightpink", opacity=1.0, flatshading=False,
        lighting=dict(ambient=0.5, diffuse=0.8, specular=0.2),
        lightposition=dict(x=100, y=200, z=150),
    )
    fig = go.Figure(data=[mesh])
    fig.update_layout(
        title="fsaverage5 inflated (Plotly, interactive)",
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode="data",
            camera=dict(eye=dict(x=-1.8, y=0, z=0)),  # lateral view
        ),
        margin=dict(l=0, r=0, t=40, b=0),
    )

    html = OUT / "03_plotly.html"
    fig.write_html(str(html), include_plotlyjs="cdn")
    print("wrote", html)

    try:
        png = OUT / "03_plotly.png"
        fig.write_image(str(png), width=700, height=600, scale=2)
        print("wrote", png)
    except Exception as exc:  # kaleido missing / failed -- HTML still produced
        print("static PNG export skipped:", exc)


if __name__ == "__main__":
    main()
