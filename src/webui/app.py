# Streamlit Web UI to drive the pipeline steps.

# GroupID-23 (22114047_22114081_22114098) - Khushal Agrawal, Rushit Pancholi and Vraj Tamkuwala
# Date: 25 Sept, 2025
# webui/app.py - Streamlit layout and controls for each algorithm step.

import time
import io
import os
import sys
import streamlit as st

# Ensure the project root is on sys.path when run via Streamlit as a script
_CURRENT_DIR = os.path.dirname(__file__)
_PROJECT_ROOT = os.path.abspath(os.path.join(_CURRENT_DIR, os.pardir))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


from pipeline import ArtGalleryPipeline
from webui.canvas_adapter import MatplotlibCanvasAdapter, PlotConfig


def get_pipeline_state():
    if "pipeline" not in st.session_state:
        adapter = MatplotlibCanvasAdapter(PlotConfig(width=7, height=7, bgcolor="#f5f5dc"))
        st.session_state.adapter = adapter
        st.session_state.pipeline = ArtGalleryPipeline(adapter)
        st.session_state.stage = "init"  # init -> polygon -> trapezoids -> monotone -> triangulation -> dual -> coloring -> guards
    return st.session_state.pipeline, st.session_state.adapter


def render_canvas(adapter: MatplotlibCanvasAdapter):
    fig = adapter.render()
    buf = io.BytesIO()
    try:
        fig.savefig(buf, format="png")
        buf.seek(0)
        st.image(buf)
    except Exception:
        # Fallback to Streamlit's pyplot if Agg fails
        st.pyplot(fig)


def main():
    st.set_page_config(page_title="Optimal Street Light Placement", layout="wide")
    st.title("Optimal Street Light Placement — Web UI")

    pipeline, adapter = get_pipeline_state()
    # We will set the live renderer after laying out columns so frames render in the right column

    # Two-column layout: controls (left), canvas (right)
    col_controls, col_canvas = st.columns([1, 3], gap="large")

    with col_controls:
        st.subheader("Controls")
        n = st.number_input("Vertices (n)", min_value=3, max_value=100, value=8, step=1, key="n_left")
        gen_disabled = False
        if st.button("1. Generate Polygon", use_container_width=True, key="gen_left", disabled=gen_disabled):
            if pipeline.step_generate_polygon_with_n(int(n)):
                st.session_state.stage = "polygon"
        st.markdown("---")
        st.subheader("Steps")
        trap_disabled = st.session_state.stage not in ["polygon", "trapezoids", "monotone", "triangulation", "dual", "coloring", "guards"]
        if st.button("2. Trapezoidalization", use_container_width=True, key="trap_left", disabled=trap_disabled):
            if pipeline.step_trapezoidalisation():
                st.session_state.stage = "trapezoids"
        mono_disabled = st.session_state.stage not in ["trapezoids", "monotone", "triangulation", "dual", "coloring", "guards"]
        if st.button("3. Monotone Partitioning", use_container_width=True, key="mono_left", disabled=mono_disabled):
            if pipeline.step_monotone_partitioning():
                st.session_state.stage = "monotone"
        tri_disabled = st.session_state.stage not in ["monotone", "triangulation", "dual", "coloring", "guards"]
        if st.button("4. Triangulation", use_container_width=True, key="tri_left", disabled=tri_disabled):
            if pipeline.step_triangulation():
                st.session_state.stage = "triangulation"
        dual_disabled = st.session_state.stage not in ["triangulation", "dual", "coloring", "guards"]
        if st.button("5. Dual Graph", use_container_width=True, key="dual_left", disabled=dual_disabled):
            if pipeline.step_dual_graph():
                st.session_state.stage = "dual"
        color_disabled = st.session_state.stage not in ["dual", "coloring", "guards"]
        if st.button("6. 3-Coloring", use_container_width=True, key="color_left", disabled=color_disabled):
            if pipeline.step_three_coloring():
                st.session_state.stage = "coloring"
        guards_disabled = st.session_state.stage not in ["coloring", "guards"]
        if st.button("7. Vertex Guards (Street Lights)", use_container_width=True, key="guards_left", disabled=guards_disabled):
            if pipeline.step_vertex_guards():
                st.session_state.stage = "guards"
        st.markdown("---")
        if st.button("Reset", use_container_width=True, key="reset_left"):
            adapter.delete("all")
            st.session_state.stage = "init"
        st.caption("Animation: 0.1s fixed")
        st.session_state.sleep = 0.1

    with col_canvas:
        placeholder = st.empty()
        def live_render(fig):
            img_buf = io.BytesIO()
            try:
                fig.savefig(img_buf, format="png")
                img_buf.seek(0)
                with placeholder:
                    st.image(img_buf)
            except Exception:
                pass
        adapter.set_live_renderer(live_render)

    # Monkey-patch time.sleep to respect slider during this session
    _original_sleep = time.sleep
    def _patched_sleep(_s):
        delay = st.session_state.sleep
        if delay and delay > 0:
            return _original_sleep(delay)
        return None
    time.sleep = _patched_sleep

    # Initial render (or final frame after interactions)
    with col_canvas:
        render_canvas(adapter)


if __name__ == "__main__":
    main()


