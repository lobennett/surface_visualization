# surface_visualization — Design

**Date:** 2026-06-23

## Purpose

A lightweight showcase repository demonstrating how to load and visualize a
single *canonical inflated cortical surface* across the major neuroimaging
tooling ecosystems. Python examples are runnable and produce verified output;
FreeSurfer and MATLAB examples are documented copy-paste snippets (those
environments are not assumed to be installed).

There is intentionally **no test suite** — the goal is a clear, comparative
reference for "how do I load an inflated surface in X?".

## The canonical asset (single source of truth)

All examples operate on the **`fsaverage` inflated surface**, fetched via
`nilearn.datasets.load_fsaverage()`. The fetch lands real files on disk in
standard formats — FreeSurfer binary geometry (`lh.inflated`) and GIFTI
(`.gii`) — so the nibabel, FreeSurfer, and MATLAB examples can all point at the
*same* downloaded asset.

`00_fetch_surface.py` downloads the asset once into `data/` and copies the
relevant `lh.inflated` / GIFTI files there for the other scripts to consume.

## Structure

```
surface_visualization/
├── README.md              # narrative index, embeds output PNGs, links each script
├── requirements.txt       # nilearn, nibabel, plotly, matplotlib
├── .gitignore             # ignores data/ download; keeps outputs/
├── data/                  # fetched fsaverage (gitignored)
├── outputs/               # rendered PNG/HTML (committed so README renders on GitHub)
├── 00_fetch_surface.py    # fetch canonical fsaverage inflated surface   [RUNNABLE]
├── 01_nilearn.py          # plot_surf / view_surf → PNG                  [RUNNABLE]
├── 02_nibabel.py          # read_geometry + GIFTI, inspect verts/faces   [RUNNABLE]
├── 03_plotly.py           # interactive 3D mesh → self-contained HTML     [RUNNABLE]
├── 04_pysurfer.md         # PySurfer/mayavi snippet + expected output    [DOCUMENTED]
├── 05_freesurfer.md       # freeview / mris_convert / mris_info CLI       [DOCUMENTED]
└── 06_matlab.md           # read_surf.m, SPM gifti(), FreeSurfer MATLAB   [DOCUMENTED]
```

## Runnable scripts

Each runnable script:
1. Loads the canonical surface from `data/`.
2. Prints a short summary (number of vertices / faces).
3. Renders a view and saves it to `outputs/`.

They run headless: matplotlib uses the `Agg` backend; plotly writes a
self-contained HTML file. No display / OpenGL is required.

## Documented files

Markdown files with copy-paste snippets and a description of expected output,
pointing at the same `data/` files. PySurfer is documented-only because
`mayavi` does not install cleanly on recent Python.

## Verification

A virtualenv is created, scripts `00`→`03` are run, output files are confirmed,
and the rendered PNGs are committed to `outputs/` and embedded in the README.

## Decisions

- **Interactive runnable tool:** plotly (renders to self-contained HTML with no
  OpenGL/display), not pyvista. PySurfer stays documented-only.
- **Commit outputs:** rendered PNGs/HTML committed to `outputs/`; the larger
  `data/` download is gitignored.
