#!/usr/bin/env python3
"""Execute Visium HD tutorial notebooks 01–08 in order with Papermill.

Run from any directory:
    python scripts/run_pipeline.py
    python scripts/run_pipeline.py --dry-run
    python scripts/run_pipeline.py --from-step 5 --to-step 8

Dependency: pip install papermill ipykernel
"""
from __future__ import annotations

import argparse
import logging
import os
import sys
import traceback
from datetime import datetime
from pathlib import Path

NOTEBOOKS = (
    "01_data_loading.ipynb",
    "02_quality_control.ipynb",
    "03_normalization.ipynb",
    "04_clustering.ipynb",
    "05_spatial_analysis.ipynb",
    "06_marker_analysis.ipynb",
    "07_biological_annotation.ipynb",
    "08_robustness_checks.ipynb",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--from-step", type=int, default=1, choices=range(1, 9), metavar="1-8")
    parser.add_argument("--to-step", type=int, default=8, choices=range(1, 9), metavar="1-8")
    parser.add_argument("--kernel", default=None, help="Jupyter kernel name (default: notebook metadata / Papermill default)")
    parser.add_argument("--dry-run", action="store_true", help="Validate inputs and print planned steps without executing")
    parser.add_argument("--project-root", type=Path, default=None, help="Project directory (default: parent of scripts/)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.from_step > args.to_step:
        print("ERROR: --from-step must not exceed --to-step", file=sys.stderr)
        return 2

    root = (args.project_root or Path(__file__).resolve().parent.parent).expanduser().resolve()
    notebook_dir = root / "notebooks"
    output_dir = root / "results" / "executed_notebooks"
    log_dir = root / "results" / "logs"
    selected = list(enumerate(NOTEBOOKS, start=1))[args.from_step - 1 : args.to_step]

    missing = [str(notebook_dir / name) for _, name in selected if not (notebook_dir / name).is_file()]
    if missing:
        print("ERROR: Missing notebook(s):\n  " + "\n  ".join(missing), file=sys.stderr)
        return 2

    print(f"Project root: {root}")
    print(f"Python: {sys.executable}")
    print(f"Steps: {args.from_step}–{args.to_step}")
    for step, name in selected:
        print(f"  {step:02d}: {name}")
    if args.dry_run:
        print("DRY RUN — no notebooks executed or files written")
        return 0

    try:
        import papermill as pm
    except ImportError:
        print("ERROR: Papermill is not installed in this Python environment.\n"
              "Install with: python -m pip install papermill ipykernel", file=sys.stderr)
        return 2

    output_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = log_dir / f"pipeline_{run_id}.log"
    logger = logging.getLogger("visium_pipeline")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    for handler in (logging.StreamHandler(sys.stdout), logging.FileHandler(log_path, encoding="utf-8")):
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # All notebooks use Path.cwd() to discover the project root.
    previous_cwd = Path.cwd()
    os.chdir(root)
    try:
        for step, name in selected:
            source = notebook_dir / name
            target = output_dir / f"{Path(name).stem}_executed_{run_id}.ipynb"
            logger.info("START %02d/08 %s", step, name)
            logger.info("Executed notebook: %s", target.relative_to(root))
            try:
                kwargs = {
                    "input_path": str(source),
                    "output_path": str(target),
                    "cwd": str(root),
                    "log_output": True,
                    "progress_bar": False,
                }
                if args.kernel:
                    kwargs["kernel_name"] = args.kernel
                pm.execute_notebook(**kwargs)
            except Exception:
                logger.error("FAILED step %02d: %s", step, name)
                logger.error("%s", traceback.format_exc())
                logger.error("Stopping pipeline; inspect %s and %s", target, log_path)
                return 1
            logger.info("PASS %02d/08 %s", step, name)
        logger.info("PIPELINE PASS — all %d selected notebooks executed", len(selected))
        logger.info("Log: %s", log_path)
        return 0
    finally:
        os.chdir(previous_cwd)


if __name__ == "__main__":
    raise SystemExit(main())