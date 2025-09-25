#!/usr/bin/env python3

# Convenience launcher for the Art Gallery project.

# GroupID-23 (22114047_22114081_22114098) - Khushal Agrawal, Rushit Pancholi and Vraj Tamkuwala
# Date: 25 Sept, 2025
# run.py - Alternate launcher mirroring main.py.

# Usage:
#   - Desktop (Tkinter):  python run.py --desktop
#   - Web (Streamlit):    python run.py --web [--port 8501]# """

import argparse
import os
import subprocess
import sys


def run_web_ui(port: int) -> int:
    """Launch the Streamlit app via the streamlit CLI."""
    # Best to invoke streamlit via module to ensure same interpreter is used
    app_path = os.path.join(os.path.dirname(__file__), "webui", "app.py")

    # Optional pre-check for streamlit to give a nicer error
    try:
        import streamlit  # noqa: F401
    except Exception as exc:  # pragma: no cover
        print("Streamlit is not installed. Please install dependencies first:")
        print("  pip install -r ./requirements.txt")
        print(f"Details: {exc}")
        return 1

    # Run from project root so local imports resolve
    repo_root = os.path.abspath(os.path.dirname(__file__))
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        app_path,
        "--server.port",
        str(port),
    ]
    return subprocess.call(cmd, cwd=repo_root)


def run_desktop_gui() -> int:
    """Run the Tkinter-based desktop GUI directly."""
    try:
        # Import inside to keep startup fast and avoid side effects before mode is chosen
        from src.controller import main as desktop_main
    except Exception as exc:  # pragma: no cover
        print(
            "Failed to import desktop GUI. Ensure you are running from the project root."
        )
        print(f"Details: {exc}")
        return 1

    try:
        desktop_main()
        return 0
    except SystemExit as se:  # pragma: no cover
        return int(getattr(se, "code", 0) or 0)
    except Exception as exc:  # pragma: no cover
        print(f"Desktop GUI crashed: {exc}")
        return 1


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Art Gallery launcher")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--web", action="store_true", help="Run the Streamlit web UI (default)"
    )
    mode.add_argument(
        "--desktop", action="store_true", help="Run the Tkinter desktop UI"
    )
    parser.add_argument(
        "--port", type=int, default=8501, help="Port for web UI (default: 8501)"
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    if args.desktop:
        return run_desktop_gui()

    # Default to web if neither flag provided
    return run_web_ui(port=args.port)


if __name__ == "__main__":
    raise SystemExit(main())
