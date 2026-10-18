# Visium HD Spatial Transcriptomics Tutorial
An exploratory Scanpy/Squidpy workflow for GEO [GSM9936742](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9936742) (HD-02), using 56-µm spatial bins. The eight notebooks cover data loading, QC, normalization, clustering, spatial analysis, markers, biological annotation, and robustness checks.

Tested: macOS Apple Silicon · Python 3.11 · `visiumHD` · 8/8 notebooks passed (2026-10-18). Windows and Linux have not been tested.


## 1. Prepare the data
Download the GSM9936742 files from GEO and place them in the project's `data/` directory using these names:

```text
data/GSM9936742_HD-02_filtered_feature_bc_matrix.h5
data/GSM9936742_HD-02_tissue_positions.parquet
data/GSM9936742_HD-02_tissue_hires_image.png
```

The H5 and parquet files are required; the image is a reference.


## 2. Install and run
Open a Conda-enabled terminal and change to the project root (the folder containing `environment.yml` and `scripts/`). Its location depends on where you saved the project.

For example, only if the folder is on your Desktop:
- macOS/Linux: `cd ~/Desktop/visium_hd_tutorial`
- Windows PowerShell: `cd "$HOME\Desktop\visium_hd_tutorial"`
- Windows CMD: `cd /d "%USERPROFILE%\Desktop\visium_hd_tutorial"`

Then run the following from the project root in your Conda-enabled terminal:

```bash
conda env create -f environment.yml
conda activate visiumHD
python -m ipykernel install --user --name visiumHD --display-name "Python (visiumHD)"
python scripts/run_pipeline.py --kernel visiumHD
```

If `visiumHD` already exists, skip the `conda env create` line. Ensure `environment.yml` specifies `name: visiumHD` before installing.

Success is indicated by:

```text
PIPELINE PASS — all 8 selected notebooks executed
```

Outputs are written to `results/adata/`, `results/figures/`, `results/tables/`, `results/executed_notebooks/`, and `results/logs/`. Rerunning may overwrite outputs; back up `results/` if needed.


## Interpretation notes
This is an exploratory bin-level analysis, not single-cell identification. QC filtering was not applied; most clusters remain biologically unresolved, and histology-image registration was not validated. Spatial dependence also limits interpretation of per-bin differential-expression tests.

Compatibility: The commands above are broadly portable, but native Windows/Linux dependency installation and pipeline execution remain unverified. The supplied environment is not a fully locked cross-platform environment.