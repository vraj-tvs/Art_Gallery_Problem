# Web UI (Streamlit)

Run the web UI:

- Install deps:
  - `pip install streamlit matplotlib`
- Start:
  - `python -m streamlit run webui/app.py`

Notes
- Uses a Matplotlib adapter that mimics the Tkinter canvas API used in algorithms.
- Sidebar buttons run each step. Use the slider to adjust animation delay.
- Reset Canvas clears current drawing; pipeline state persists in the session.
