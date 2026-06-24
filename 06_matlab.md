# MATLAB (documented)

Two common MATLAB routes to load an inflated surface: FreeSurfer's bundled
MATLAB helpers (for binary geometry) and SPM's `gifti` toolbox (for `.gii`).

> Not runnable in this repo (no MATLAB), but these are the canonical snippets.

## 1. FreeSurfer's `read_surf.m`

FreeSurfer ships MATLAB readers under `$FREESURFER_HOME/matlab`. Add them to the
path, then read the binary geometry directly:

```matlab
addpath(fullfile(getenv('FREESURFER_HOME'), 'matlab'));

surf = fullfile(getenv('SUBJECTS_DIR'), 'fsaverage', 'surf', 'lh.inflated');
[vertices, faces] = read_surf(surf);

% FreeSurfer faces are 0-based; MATLAB is 1-based.
faces = faces + 1;

fprintf('%d vertices, %d faces\n', size(vertices, 1), size(faces, 1));
trisurf(faces, vertices(:,1), vertices(:,2), vertices(:,3), ...
        'EdgeColor', 'none', 'FaceColor', [0.8 0.8 0.8]);
axis equal off; camlight; lighting gouraud;
title('fsaverage inflated (FreeSurfer read\_surf)');
```

## 2. SPM's `gifti` toolbox (GIFTI files)

The [`gifti`](https://www.artefact.tk/software/matlab/gifti/) toolbox (bundled
with SPM) reads the `.gii` produced by `mris_convert` or by this repo's
`00_fetch_surface.py`:

```matlab
g = gifti('lh.inflated.surf.gii');   % or data/left.inflated.gii.gz (gunzip first)

vertices = g.vertices;   % N x 3
faces    = g.faces;      % M x 3 (already 1-based)

fprintf('%d vertices, %d faces\n', size(vertices, 1), size(faces, 1));
patch('Vertices', vertices, 'Faces', faces, ...
      'FaceColor', [0.8 0.8 0.8], 'EdgeColor', 'none');
axis equal off; camlight; lighting gouraud;
```

> The GIFTI files in `data/` are gzipped (`.gii.gz`). Gunzip first
> (`gunzip data/left.inflated.gii.gz`), or convert an uncompressed
> `.surf.gii` with `mris_convert`.

## Expected output

Both routes print the vertex/face counts (`10242` / `20480` for `fsaverage5`,
`163842` / `327680` for full `fsaverage`) and render a shaded inflated
hemisphere in a MATLAB figure window.
