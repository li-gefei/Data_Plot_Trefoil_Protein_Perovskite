from pathlib import Path

import matplotlib as mpl
import numpy as np

mpl.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colorbar import Colorbar


folder = Path(__file__).resolve().parent

mpl.rcParams.update({
    "font.family": "Arial",
    "font.size": 14,
    "axes.labelsize": 15,
    "axes.linewidth": 1.1,
    "axes.spines.top": True,
    "axes.spines.right": True,
    "axes.spines.bottom": True,
    "axes.spines.left": True,
    "mathtext.fontset": "custom",
    "mathtext.rm": "Arial",
    "mathtext.it": "Arial:italic",
    "mathtext.fallback": None,
    "svg.fonttype": "none",
    "svg.hashsalt": "Vector_Field_Reconstruction",
})
Colorbar.n_rasterize = 10**9


def intensity_bar(fig, image, axis, horizontal, longitudinal):
    ticks = [0, 0.00035, 0.0007, 0.00105, 0.0014] if longitudinal else [0, .5, 1, 1.5, 2]
    orientation = "horizontal" if horizontal else "vertical"
    bar = fig.colorbar(image, cax=axis, orientation=orientation, ticks=ticks)
    if longitudinal:
        bar.set_ticks(ticks, labels=["0", "0.35", "0.70", "1.05", "1.40"])
    label = r"$I_z/I_0$ ($\times 10^{-3}$)" if longitudinal else r"$(I_x+I_y)/I_0$"
    bar.solids.set_edgecolor("face")
    bar.solids.set_linewidth(.06)
    bar.set_label(label, labelpad=8)
    if horizontal:
        axis.xaxis.set_ticks_position("top")
        axis.xaxis.set_label_position("top")


def focus(data):
    fig = plt.figure(figsize=(9.4, 5.05))
    size = 3.24 / 5.05
    left, right, bottom, top = data["focus_view"]
    for j, x0 in enumerate((.085, .556)):
        heat = fig.add_axes((x0, .135, 3.24 / 9.4, size))
        color = fig.add_axes((x0, .813, 3.24 / 9.4, .031))
        values = data["focus"][j]
        extent = data["focus_extent"]
        rows, columns = values.shape
        x_edges = np.linspace(extent[0], extent[1], columns + 1)
        y_edges = np.linspace(extent[2], extent[3], rows + 1)
        image = heat.pcolormesh(
            x_edges, y_edges, values, shading="flat", edgecolors="face", linewidth=.06,
            cmap="magma", vmin=0, vmax=data["limits"][j],
        )
        heat.set(
            xlim=(left, right), ylim=(bottom, top), aspect="equal", xticks=[-1, 0, 1],
            yticks=[-1, 0, 1], xlabel=r"$x/w_{\mathrm{beam}}$",
        )
        if j == 0:
            heat.set_ylabel(r"$y/w_{\mathrm{beam}}$")
            heat.add_collection(LineCollection(data["trefoils"], colors="white", linewidths=.58, alpha=.98))
        else:
            heat.yaxis.tick_right()
        intensity_bar(fig, image, color, horizontal=True, longitudinal=j == 1)
    return fig


def xz(data):
    fig = plt.figure(figsize=(10.7, 6.9))
    for j, y0 in enumerate((.557, .130)):
        heat = fig.add_axes((.104, y0, .748, .386))
        color = fig.add_axes((.880, y0, .018, .386))
        image = heat.imshow(
            data["xz"][j], origin="lower", extent=data["xz_extent"], aspect="auto",
            interpolation="nearest", cmap="magma", vmin=0, vmax=data["limits"][j],
        )
        heat.axvline(0, color="white", linewidth=.6, alpha=.7)
        heat.set(
            ylabel=r"$x$ ($\mathrm{\mu m}$)", xticks=[-300, -200, -100, 0, 100, 200, 300],
            yticks=[-30, -20, -10, 0, 10, 20, 30],
        )
        heat.tick_params(axis="x", labelbottom=j == 1, pad=6)
        if j == 1:
            heat.set_xlabel(r"$z$ ($\mathrm{\mu m}$)")
        intensity_bar(fig, image, color, horizontal=False, longitudinal=j == 1)
    return fig


if __name__ == "__main__":
    with np.load(folder / "data.npz", allow_pickle=False) as data:
        for draw in (focus, xz):
            fig = draw(data)
            fig.savefig(folder / f"{draw.__name__}.svg", dpi=300, metadata={"Date": None, "Creator": None})
            plt.close(fig)
