#!/usr/bin/env python3
"""Execute the TypeScript router checks under the installed OMP runtime."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER = "Runtime router checks passed:"


def main() -> int:
    omp = shutil.which("omp")
    if not omp:
        print("Runtime router check skipped: omp is not installed.", file=sys.stderr)
        return 2

    command = [
        omp,
        "--mode=rpc",
        "--no-ui",
        "--no-extensions",
        "--no-context-files",
        "--no-skills",
        "--no-tools",
        "--no-session",
        "-e",
        "tests/runtime-router-check.ts",
    ]
    result = subprocess.run(command, cwd=ROOT, input="", capture_output=True, text=True, check=False)
    output = result.stdout + result.stderr
    if MARKER not in output or "Failed to load extension" in output:
        print(output, file=sys.stderr, end="")
        print("OMP did not execute the runtime router checks cleanly.", file=sys.stderr)
        return 1
    if result.returncode != 0:
        print(output, file=sys.stderr, end="")
        print(f"Unexpected OMP exit code {result.returncode}.", file=sys.stderr)
        return 1

    marker_line = next(line for line in output.splitlines() if line.startswith(MARKER))
    print(marker_line)
    print("OMP runtime load passed in headless RPC mode; no model request was sent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
