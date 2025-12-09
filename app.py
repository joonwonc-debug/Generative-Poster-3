import random
import math
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from io import BytesIO
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="NoiseTouch Poster", layout="wide")

# -----------------------
# Functions
# -----------------------
def random_palette(k=7):
    return [(random.random(), random.random(), random.random()) for _ in range(k)]

def blob(center=(0.5, 0.5), r=0.3, points=180, wobble=0.08):
    angles = np.linspace(0, 2 * math.pi, points)
    radii = r * (1 + wobble * (np.random.rand(points) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

def draw_poster(blobs):
    fig, ax = plt.subplots(figsize=(7, 10))
    ax.set_facecolor((0.98, 0.98, 0.97))
    ax.axis("off")

    for b in blobs:
        x, y = blob(center=b["center"], r=b["r"], wobble=b["wobble"])
        ax.fill(x, y, color=b["color"], alpha=b["alpha"], edgecolor=(0, 0, 0, 0))

    ax.text(
        0.05, 0.95,
        "NoiseTouch Generative Poster",
        fontsize=16, weight="bold", transform=ax.transAxes
    )
    ax.text(
        0.05, 0.91,
        "Week 4 • Arts & Advanced Big Data",
        fontsize=10, transform=ax.transAxes
    )
    return fig

def fig_to_png(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    buf.seek(0)
    return buf


# -----------------------
# Session State
# -----------------------
if "palette" not in st.session_state:
    st.session_state.palette = random_palette()

if "blobs" not in st.session_state:
    st.session_state.blobs = []


# -----------------------
# Sidebar controls
# -----------------------
st.sidebar.header("Controls")

n_layers = st.sidebar.slider("Initial Layers", 1, 30, 12)
wobble = st.sidebar.slider("Wobble", 0.05, 0.5, 0.25)

if st.sidebar.button("Generate New Poster"):
    st.session_state.blobs = []
    for _ in range(n_layers):
        cx, cy = random.random(), random.random()
        r = random.uniform(0.15, 0.45)
        st.session_state.blobs.append({
            "center": (cx, cy),
            "r": r,
            "wobble": wobble,
            "color": random.choice(st.session_state.palette),
            "alpha": random.uniform(0.3, 0.6),
        })


# -----------------------
# Draw main figure
# -----------------------
fig = draw_poster(st.session_state.blobs)
png = fig_to_png(fig)

st.write("### Click inside the canvas to add a blob:")

canvas_result = st_canvas(
    background_image=png,
    height=900,
    width=600,
    drawing_mode="point",
    key="canvas",
)

# -----------------------
# Process Click Event
# -----------------------
if canvas_result.json_data is not None:

    objects = canvas_result.json_data.get("objects", [])

    if len(objects) > 0:
        last_obj = objects[-1]

        cx = last_obj["left"] / 600       # convert to 0–1 normalized
        cy = last_obj["top"] / 900

        st.session_state.blobs.append({
            "center": (cx, cy),
            "r": random.uniform(0.1, 0.3),
            "wobble": random.uniform(0.1, 0.3),
            "color": random.choice(st.session_state.palette),
            "alpha": random.uniform(0.3, 0.6),
        })

        st.experimental_rerun()
