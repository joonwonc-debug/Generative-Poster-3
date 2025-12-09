import random
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

def random_palette(k=7):
    return [(random.random(), random.random(), random.random()) for _ in range(k)]

def blob(center=(0.5, 0.5), r=0.3, points=180, wobble=0.08):
    angles = np.linspace(0, 2*math.pi, points)
    radii = r * (1 + wobble * (np.random.rand(points)-0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

def draw_poster(ax, n_layers=12, wobble_range=(0.15,0.35), palette=None):
    ax.clear()
    ax.set_facecolor((0.98,0.98,0.97))
    ax.axis('off')

    if palette is None:
        palette = random_palette()

    for _ in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(0.15, 0.45)
        wobble = random.uniform(*wobble_range)
        x, y = blob(center=(cx, cy), r=rr, wobble=wobble)
        color = random.choice(palette)
        alpha = random.uniform(0.3, 0.6)
        ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0,0,0,0))

    ax.text(0.05, 0.95, "NoiseTouch Generative Poster", fontsize=16, weight='bold', transform=ax.transAxes)
    ax.text(0.05, 0.91, "Week 4 • Arts & Advanced Big Data", fontsize=10, transform=ax.transAxes)
    plt.draw()

def on_click(event, ax, palette):
    if event.inaxes != ax:
        return
    x, y = blob(center=(event.xdata, event.ydata), r=random.uniform(0.1,0.3), wobble=random.uniform(0.1,0.3))
    color = random.choice(palette)
    ax.fill(x, y, color=color, alpha=random.uniform(0.3,0.6), edgecolor=(0,0,0,0))
    plt.draw()

def interactive_poster():
    fig, ax = plt.subplots(figsize=(7,10))
    plt.subplots_adjust(left=0.25, bottom=0.25)

    palette = random_palette()

    ax_layers = plt.axes([0.25, 0.15, 0.65, 0.03])
    ax_wobble = plt.axes([0.25, 0.10, 0.65, 0.03])

    slider_layers = Slider(ax_layers, 'Layers', 1, 30, valinit=12, valstep=1)
    slider_wobble = Slider(ax_wobble, 'Wobble', 0.05, 0.5, valinit=0.25)

    def update(val):
        n_layers = int(slider_layers.val)
        wobble_val = slider_wobble.val
        draw_poster(ax, n_layers=n_layers, wobble_range=(wobble_val, wobble_val), palette=palette)

    slider_layers.on_changed(update)
    slider_wobble.on_changed(update)

    fig.canvas.mpl_connect('button_press_event', lambda event: on_click(event, ax, palette))

    draw_poster(ax, palette=palette)
    plt.show()

interactive_poster()
