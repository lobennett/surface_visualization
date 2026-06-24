# FreeSurfer CLI (documented)

[FreeSurfer](https://surfer.nmr.mgh.harvard.edu/) is the canonical
surface-reconstruction suite. Its `fsaverage` subject ships with the inflated
surfaces every other tool here approximates. These commands assume a FreeSurfer
install with `$FREESURFER_HOME` set and `$SUBJECTS_DIR` pointing at the subjects
directory.

> Not runnable in this repo because FreeSurfer is a large native install, but
> these are the standard, copy-paste commands.

## Where the canonical inflated surface lives

```bash
$SUBJECTS_DIR/fsaverage/surf/lh.inflated
$SUBJECTS_DIR/fsaverage/surf/rh.inflated
```

These are FreeSurfer **binary geometry** files (not GIFTI).

## Inspect the surface

```bash
# Vertex / face counts and geometry metadata.
mris_info $SUBJECTS_DIR/fsaverage/surf/lh.inflated
```

## Interactive visualization with freeview

```bash
freeview -f $SUBJECTS_DIR/fsaverage/surf/lh.inflated:edgecolor=overlay
```

Or the older `tksurfer`:

```bash
tksurfer fsaverage lh inflated
```

## Convert to GIFTI (to interoperate with the Python examples)

`mris_convert` turns the FreeSurfer binary surface into a `.surf.gii` that
nibabel / nilearn / Plotly can load directly:

```bash
mris_convert $SUBJECTS_DIR/fsaverage/surf/lh.inflated lh.inflated.surf.gii
```

The reverse also works:

```bash
mris_convert lh.inflated.surf.gii lh.inflated
```

## Expected output

`mris_info` prints `num vertices = 163842` (full-resolution `fsaverage`) or
`10242` for `fsaverage5`; `freeview` opens an interactive 3D inflated hemisphere.
