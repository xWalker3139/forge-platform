"""Generate a new golden-path service without overwriting existing work."""

import argparse
import json
import re
import shutil
from pathlib import Path


def scaffold(name, owner, destination, bundle):
    if not re.fullmatch(r"[a-z][a-z0-9-]{1,39}", name):
        raise ValueError("name must be 2-40 lowercase letters, digits or hyphens")
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,38}", owner):
        raise ValueError("invalid owner")
    target = Path(destination) / name
    if target.exists():
        raise FileExistsError(f"refusing to overwrite {target}")
    source = Path(bundle) / "forge-demo-service"
    chart = Path(bundle) / "forge-gitops" / "charts" / "forge-service"
    if (
        not (source / "pyproject.toml").is_file()
        or not (chart / "Chart.yaml").is_file()
    ):
        raise FileNotFoundError(
            "bundle must contain the demo service and the GitOps chart"
        )
    shutil.copytree(
        source,
        target,
        ignore=shutil.ignore_patterns(
            ".venv", "__pycache__", ".pytest_cache", ".ruff_cache", ".git"
        ),
    )
    shutil.copytree(chart, target / "deploy" / "chart")
    values = f"image:\n  repository: ghcr.io/{owner.lower()}/{name}\n  tag: REPLACE_WITH_COMMIT_SHA\nfaultInjection: false\n"
    (target / "deploy" / "values.yaml").write_text(values, encoding="utf-8")
    metadata = {
        "name": name,
        "owner": owner,
        "type": "service",
        "lifecycle": "experimental",
        "template": "forge-v0.1",
    }
    (target / "service-catalog.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    return target


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--owner", required=True)
    parser.add_argument("--output", default="generated")
    parser.add_argument(
        "--bundle", type=Path, default=Path(__file__).resolve().parents[2]
    )
    args = parser.parse_args()
    print(scaffold(args.name, args.owner, args.output, args.bundle))
