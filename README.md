## Art Gallery Problem — Interactive Visualization

GroupID-23 (22114047_22114081_22114098) - Khushal Agrawal, Rushit Pancholi and Vraj Tamkuwala
Date: 25 Sept, 2025

This project provides an interactive visualization of the methodology described in `Final_report.pdf` (included). It explores the Art Gallery/Street Light Placement problem on a simple polygon.

It walks through:

- Generating a random simple polygon with N vertices
- Trapezoidalisation of the polygon
- Monotone partitioning
- Triangulation of the polygon
- Dual graph construction over triangles
- 3-coloring of the triangulation
- Vertex guards selection and display

### Run Options
You can use either a browser-based app (Streamlit) or a desktop GUI (Tkinter).

### Setup
Prerequisites:
- Python 3.10+

Create a virtual environment (recommended) and install dependencies:
```bash
# From this folder
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

Alternatively, with conda:
```bash
conda create -n artgallery python=3.12 -y
conda activate artgallery
pip install -r requirements.txt
```

### Start the Web App (Streamlit)
```bash
# From this folder
python -m streamlit run src/webui/app.py
```
Open the local URL printed in the terminal (typically `http://localhost:8501`).

Usage in the web UI:
- Set the number of vertices and click "Generate Polygon".
- Step through: Trapezoidalisation → Monotone Partitioning → Triangulation → Dual Graph → 3 Coloring → Vertex Guards.
- Click "Reset Canvas" to start over.

Or use the unified launcher:
```bash
python main.py --web --port 8501
```

### Start the Desktop GUI (Tkinter)
```bash
# From this folder
python main.py --desktop
```

You can also use the helper script to set up a venv and run:
```bash
./setup_and_run.sh --web   # or --desktop
```

### Project Structure
```
Art_Gallery_Problem/
├── main.py                     # Main entry point with CLI launcher
├── run.py                      # Alternative runner script
├── setup_and_run.sh           # Setup script for bash environments
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── .venv/                     # Virtual environment (created after setup)
└── src/                       # Main application source code
    ├── __init__.py
    ├── __main__.py
    ├── controller.py          # Tkinter desktop GUI controller
    ├── pipeline.py            # Orchestrates algorithmic steps
    ├── ui.py                  # Desktop UI components
    ├── dcel.py               # DCEL data structure and drawing helpers
    ├── generate_polygon.py   # Random polygon generation
    ├── trapezoidalisation.py # Trapezoidal decomposition algorithm
    ├── monotone_partitioning.py # Monotone polygon partitioning
    ├── triangulation.py      # Polygon triangulation
    ├── dual_graph.py        # Dual graph construction over triangles
    ├── three_coloring.py    # 3-coloring of triangulation
    ├── vertex_guards.py     # Vertex guards selection algorithm
    └── webui/               # Streamlit web interface
        ├── __init__.py
        ├── app.py          # Main Streamlit application
        ├── canvas_adapter.py # Canvas abstraction for web UI
        └── README.md       # Web UI specific documentation
```

### UI flow and naming (per the PDF)
- 1. Generate Polygon
- 2. Trapezoidalization
- 3. Monotone Partitioning
- 4. Triangulation (diagonals shown as dotted lines)
- 5. Dual Graph
- 6. 3-Coloring (palette: `#b58900`, `#228b22`, `#d33682`)
- 7. Vertex Guards (Street Lights) — displayed in red markers with white center for visibility

The web UI mimics a canvas via Matplotlib and follows the pipeline described in the PDF.

### Troubleshooting
- If Streamlit doesn’t open automatically, copy the "Local URL" shown in the terminal into your browser.
- If rendering looks odd, ensure you have a recent Matplotlib installed.
- On macOS with multiple Python installs, ensure the interpreter that installed dependencies runs the commands.
