from pathlib import Path

import matplotlib as mpl
import numpy as np

mpl.use("Agg")

import matplotlib.pyplot as plt


folder = Path(__file__).resolve().parent
mpl.rcParams.update({
    "font.family": "Arial",
    "mathtext.fontset": "custom",
    "mathtext.rm": "Arial",
    "mathtext.it": "Arial:italic",
    "mathtext.fallback": None,
    "font.size": 14,
    "axes.labelsize": 15,
    "axes.linewidth": 1.1,
    "axes.spines.top": True,
    "axes.spines.right": True,
    "svg.fonttype": "none",
    "svg.hashsalt": "UVFS",
})


def save(fig, image, name, label, ticks, tick_labels=None):
    axis = fig.add_axes((.867, .24, .021, .56))
    bar = fig.colorbar(image, cax=axis, ticks=ticks)
    bar.solids.set_rasterized(False)
    bar.solids.set_edgecolor("face")
    bar.solids.set_linewidth(.06)
    if tick_labels is not None:
        bar.set_ticks(ticks, labels=tick_labels)
    bar.set_label(label, labelpad=9)
    fig.savefig(folder / f"{name}.svg", dpi=300, metadata={"Date": None, "Creator": None})
    plt.close(fig)


def maps(data, name, label, cmap, limits, ticks, tick_labels=None):
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.9), sharex=True, sharey=True)
    fig.subplots_adjust(left=.115, right=.827, top=.87, bottom=.185, wspace=.16)
    extent = data["extent"]
    for ax, values, side in zip(axes, data[name], data["side"]):
        rows, columns = values.shape
        x_edges = np.linspace(extent[0], extent[1], columns + 1)
        y_edges = np.linspace(extent[3], extent[2], rows + 1)
        image = ax.pcolormesh(
            x_edges, y_edges, values, shading="flat", edgecolors="face", linewidth=.06,
            cmap=cmap, vmin=limits[0], vmax=limits[1],
        )
        ax.set(xlim=extent[:2], ylim=extent[2:], aspect="equal")
        ax.set(xticks=[700, 725, 750], yticks=[650, 675, 700])
        ax.annotate(
            side, (.5, 1), xycoords="axes fraction", xytext=(0, 7),
            textcoords="offset points", ha="center", va="bottom", fontsize=15,
        )
    fig.supxlabel("Pixel", x=.471, y=.037)
    axes[0].set_ylabel("Pixel")
    save(fig, image, name, label, ticks, tick_labels)


def cd_map(data):
    fig = plt.figure(figsize=(7.4, 3.95))
    ax = fig.add_axes((.116, .207, .711, .70))
    image = ax.pcolormesh(
        data["cd_phase"], data["azimuth"], data["cd"], cmap="RdBu_r",
        vmin=-7, vmax=7, shading="flat", edgecolors="face", linewidth=.06,
    )
    ax.set(
        xlim=(0, 2*np.pi), ylim=(0, 360), xlabel="Phase (rad)",
        ylabel=r"Azimuth ($\degree$)", yticks=[0, 90, 180, 270, 360],
    )
    ax.tick_params(axis="x", pad=6)
    ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi], labels=["0", r"$\pi/2$", r"$\pi$", r"$3\pi/2$", r"$2\pi$"])
    save(fig, image, "cd", "CD (%)", [-6, -3, 0, 3, 6])


if __name__ == "__main__":
    with np.load(folder / "data.npz", allow_pickle=False) as data:
        maps(data, "beam", "Normalized intensity", "magma", (0, 1), [0, .25, .5, .75, 1])
        maps(data, "amp", r"$m=1$ amplitude", "magma", (0, 70), [0, 20, 40, 60])
        maps(data, "phase", r"$m=1$ phase (rad)", "twilight", (-np.pi, np.pi), [-np.pi, 0, np.pi], [r"$-\pi$", "0", r"$\pi$"])
        cd_map(data)
