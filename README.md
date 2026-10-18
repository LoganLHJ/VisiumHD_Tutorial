# Visium HD Spatial Transcriptomics Tutorial
An exploratory, reproducible Scanpy/Squidpy workflow for the public GEO dataset [GSM9936742 (HD-02)](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9936742), analyzed using 56-µm spatial bins.

This tutorial is intended for researchers getting started with Visium HD spatial transcriptomics. You can run all eight notebooks automatically or explore them interactively in JupyterLab.

Tested configuration: macOS (Apple Silicon), Python 3.11, Conda environment `visiumHD`. All eight notebooks passed on 2026-10-18. Windows and Linux have not been tested.

> Scope: This is an exploratory bin-level workflow, not single-cell identification. The original GitHub workflow does not perform Tangram mapping or reference-based cell-type deconvolution.


## 1. Workflow overview
| Notebook | Purpose |
| --- | --- |
| `01_data_loading.ipynb` | Load expression data and spatial coordinates |
| `02_quality_control.ipynb` | Inspect quality-control metrics |
| `03_normalization.ipynb` | Normalize and transform expression data |
| `04_clustering.ipynb` | Explore expression-based clusters |
| `05_spatial_analysis.ipynb` | Examine spatial patterns |
| `06_marker_analysis.ipynb` | Identify candidate cluster marker genes |
| `07_biological_annotation.ipynb` | Explore marker-based biological annotations |
| `08_robustness_checks.ipynb` | Check robustness of exploratory findings |

Run notebooks in numerical order. Later steps may depend on files produced by earlier ones.


## 2. Download the project
Install [Git](https://git-scm.com/) and a Conda distribution such as [Miniforge](https://github.com/conda-forge/miniforge) if you do not already have them.

In a Conda-enabled terminal, run:

```bash
git clone https://github.com/LoganLHJ/VisiumHD_Tutorial.git
cd VisiumHD_Tutorial
```

If you downloaded the repository as a ZIP file instead, extract it and open a terminal in the extracted project folder. All commands below should be run from the project root (the directory containing `environment.yml`, `notebooks/`, and `scripts/`).

To check your location:

```bash
ls
```

You should see `environment.yml`, `notebooks`, and `scripts` (on Windows, use `dir` instead of `ls` if needed).


## 3. Prepare the input data
This tutorial uses the following files from [GEO GSM9936742](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9936742):

```text
data/
├── GSM9936742_HD-02_filtered_feature_bc_matrix.h5
├── GSM9936742_HD-02_tissue_positions.parquet
└── GSM9936742_HD-02_tissue_hires_image.png
```

The H5 expression matrix and parquet spatial coordinates are required. The high-resolution tissue image is provided as a reference.

Check whether these files are already included in your downloaded project. If any are missing, download them from the GEO record and place them in `data/` with exactly the filenames shown above. Do not rename or decompress the H5 file unless you also update the code.


## 4. Create the Conda environment
From the project root:

```bash
conda env create -f environment.yml
conda activate visiumHD
```

If the `visiumHD` environment already exists, skip the creation command and activate it directly.

Register the environment as a Jupyter kernel:

```bash
python -m ipykernel install --user --name visiumHD --display-name "Python (visiumHD)"
```

The environment file should specify `name: visiumHD`. Dependency resolution can differ across platforms; successful installation and execution have only been verified on the tested macOS configuration.


## 5. Run the analysis — choose one method
Both methods use the same eight notebooks and the same input data. You only need to choose one method, although you can use both.


### Option A — Run the entire pipeline automatically
Best for: Reproducing the complete workflow and generating outputs without opening notebooks individually.

From the project root, with the environment activated:

```bash
conda activate visiumHD
python scripts/run_pipeline.py --kernel visiumHD
```

The runner executes notebooks `01` through `08` in order. A successful run ends with:

```text
PIPELINE PASS — all 8 selected notebooks executed
```

Review the execution log in `results/logs/` if a notebook fails. Correct the reported error before rerunning the pipeline.


### Option B — Explore and execute notebooks in JupyterLab
Best for: Learning how the analysis works, checking intermediate results, and modifying code or parameters one cell at a time.

From the project root, with the environment activated:

```bash
conda activate visiumHD
jupyter lab
```

If `jupyter lab` is not available, install JupyterLab in the active environment:

```bash
conda install -c conda-forge jupyterlab
```

JupyterLab usually opens automatically in your browser. Otherwise, copy the local URL shown in the terminal (often starting with `http://localhost:8888/lab`) and open it in your browser. The analysis runs on your computer, not on a remote cloud service.

In JupyterLab:

1. Open the `notebooks/` directory.
2. Open `01_data_loading.ipynb`.
3. Select the Python (visiumHD) kernel in the notebook's kernel selector.
4. Run each cell in order using Shift + Enter, and inspect its outputs.
5. Continue with notebooks `02` through `08` in numerical order.

If you change analysis parameters, downstream notebooks may need to be rerun. Some notebooks read intermediate results saved by previous notebooks, so do not skip earlier steps on a fresh project.

To stop JupyterLab, return to the terminal where it is running and press Ctrl + C.


## 6. Where to find results
Generated files are stored under `results/`:

| Directory | Contents |
| --- | --- |
| `results/adata/` | Processed AnnData objects and intermediate analysis data |
| `results/figures/` | Analysis plots and spatial visualizations |
| `results/tables/` | QC summaries, marker tables, and other tabular outputs |
| `results/executed_notebooks/` | Notebooks saved with outputs from automated execution |
| `results/logs/` | Pipeline execution logs |

The `results/` directory is ignored by Git. Rerunning analyses may overwrite existing results, so make a backup if you need to preserve a particular run.


## 7. Interpretation and limitations
- Spatial bins are not individual cells. A 56-µm bin may contain multiple cells or cell types.
- QC filtering was not applied. The QC notebook explores quality metrics, but results should not be interpreted as having passed a formal filtering procedure.
- Most clusters remain biologically unresolved. Marker-based labels are exploratory hypotheses, not validated cell identities.
- Histology-image registration was not validated. Do not treat image overlays as independently verified anatomical registration.
- Spatial dependence affects statistical interpretation. Nearby bins are not necessarily independent, which limits conventional per-bin differential-expression conclusions.
- No Tangram or reference-based mapping is included. This repository intentionally retains the original eight-notebook Scanpy/Squidpy workflow.

This tutorial is intended for education and exploratory analysis, not clinical or diagnostic use.


## 8. Troubleshooting
`cd: no such file or directory` — Check where you cloned or extracted the repository. Use the actual folder name and path; do not assume it is located on your Desktop.

`conda: command not found` — Install a Conda distribution and reopen a Conda-enabled terminal.

`No such file or directory` for a GEO input file — Check that all required files are present under `data/` and that filenames match exactly.

Jupyter kernel `visiumHD` is missing — Activate the environment and rerun the `ipykernel install` command in Section 4.

`jupyter: command not found` — Activate `visiumHD` and install JupyterLab as described in Option B.

A later notebook fails when run by itself — Run earlier notebooks in order to generate the intermediate files it expects.

---

Dataset: [GEO GSM9936742](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9936742)  
Repository: [LoganLHJ/VisiumHD_Tutorial](https://github.com/LoganLHJ/VisiumHD_Tutorial)
