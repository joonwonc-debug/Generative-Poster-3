import random
import math
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

st.set_page_config(page_title="NoiseTouch Generative Poster", layout="centered")

def random_palette(k=7):
    return [(random.random(), random.random(), random.random()) for _ in range(k)]

def blob(center=(0.5, 0.5), r=0.3, points=180, wobble=0.08):
    angles = np.linspace(0, 2*math.pi, points)
    radii = r * (1 + wobble * (np.random.rand(points)-0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

def draw_poster(blobs):
    fig, ax = plt.subplots(figsize=(7,10))
    ax.set_facecolor((0.98,0.98,0.97))
    ax.axis('off')

    for b in blobs:
        x, y = blob(center=b["center"], r=b["r"], wobble=b["wobble"])
        ax.fill(x, y, color=b["color"], alpha=b["alpha"], edgecolor=(0,0,0,0))

    ax.text(0.05, 0.95, "NoiseTouch Generative Poster", fontsize=16, weight='bold', transform=ax.transAxes)
    ax.text(0.05, 0.91, "Week 4 • Arts & Advanced Big Data", fontsize=10, transform=ax.transAxes)
    return fig

# -----------------------------
# SESSION STATE
# -----------------------------
if "palette" not in st.session_state:
    st.session_state.palette = random_palette()

if "blobs" not in st.session_state:
    st.session_state.blobs = []

# -----------------------------
# SIDEBAR UI
# -----------------------------
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

# -----------------------------
# DRAW FIGURE
# -----------------------------
fig = draw_poster(st.session_state.blobs)
st.pyplot(fig, use_container_width=False)

# -----------------------------
# CLICK TO ADD BLOB
# -----------------------------
coords = streamlit_image_coordinates(fig)

if coords is not None:
    # Matplotlib figure coordinates are normalized (0~1)
    x = coords["x"] / fig.bbox.width
    y = 1 - (coords["y"] / fig.bbox.height)

    st.session_state.blobs.append({
        "center": (x, y),
        "r": random.uniform(0.1, 0.3),
        "wobble": random.uniform(0.1, 0.3),
        "color": random.choice(st.session_state.palette),
        "alpha": random.uniform(0.3, 0.6),
    })

    st.experimental_rerun()
