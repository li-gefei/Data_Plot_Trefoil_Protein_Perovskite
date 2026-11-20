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
    "axes.linewidth": 1.1,
    "axes.spines.top": True,
    "axes.spines.right": True,
    "xtick.major.width": 1.1,
    "ytick.major.width": 1.1,
    "svg.fonttype": "none",
    "svg.hashsalt": "Liquid_Perovskite",
})


def position_labels(axes, labels):
    for ax, label in zip(axes, labels):
        ax.annotate(
            label, (0.5, 1), xycoords="axes fraction", xytext=(0, 7),
            textcoords="offset points", ha="center", va="bottom", fontsize=15,
        )


def save(fig, image, name, label, ticks, tick_labels=None):
    color_ax = fig.add_axes((0.915, 0.24, 0.013, 0.57))
    color = fig.colorbar(image, cax=color_ax, ticks=ticks)
    color.solids.set_rasterized(False)
    color.solids.set_edgecolor("face")
    color.solids.set_linewidth(.06)
    if tick_labels is not None:
        color.set_ticks(ticks, labels=tick_labels)
    color.set_label(label, labelpad=10)
    fig.savefig(folder / f"{name}.svg", dpi=300, metadata={"Date": None, "Creator": None})
    plt.close(fig)


def spatial(data, name, label, cmap, limits, ticks, tick_labels=None):
    fig = plt.figure(figsize=(15.8, 8.45))
    blocks = fig.add_gridspec(2, 1, left=0.086, right=0.895, bottom=0.086, top=0.947, hspace=0.255)
    extent = data["extent"]
    labels = data["position"]
    sides = data["side"]
    images = data[name]

    for index, block in enumerate(blocks):
        columns = slice(index * 7, (index + 1) * 7)
        axes = block.subgridspec(2, 7, wspace=0.095, hspace=0.095).subplots(sharex=True, sharey=True)
        position_labels(axes[0], labels[columns])
        for row, maps, side in zip(axes, images[:, columns], sides):
            for ax, values in zip(row, maps):
                rows, columns = values.shape
                x_edges = np.linspace(extent[0], extent[1], columns + 1)
                y_edges = np.linspace(extent[3], extent[2], rows + 1)
                image = ax.pcolormesh(
                    x_edges, y_edges, values, shading="flat", edgecolors="face", linewidth=.06,
                    cmap=cmap, vmin=limits[0], vmax=limits[1],
                )
                ax.set(xlim=extent[:2], ylim=extent[2:], aspect="equal")
                ax.set(xticks=[430, 445, 460], yticks=[260, 280, 300])
            box = row[0].get_position()
            fig.text(
                0.042, box.y0 + box.height / 2, side,
                ha="center", va="center", fontsize=16, fontweight="bold",
            )

    fig.supxlabel("Pixel", x=0.4905, y=0.023, fontsize=15)
    fig.supylabel("Pixel", x=0.012, y=0.5165, fontsize=15)
    save(fig, image, name, label, ticks, tick_labels)


def cd_map(data, name, label, cmap, limits, ticks):
    fig, axes = plt.subplots(2, 7, figsize=(15.8, 5.65), sharex=True, sharey=True)
    fig.subplots_adjust(left=0.064, right=0.895, bottom=0.152, top=0.928, wspace=0.245, hspace=0.270)
    labels = data["position"]
    phase = data["cd_phase"]
    azimuth = data["azimuth"]
    phase_ticks = [-2 * np.pi, -np.pi, 0, np.pi, 2 * np.pi]

    position_labels(axes[0], labels[:7])
    position_labels(axes[1], labels[7:])
    for ax, phase_edges, values in zip(axes.flat, phase, data[name]):
        image = ax.pcolormesh(
            phase_edges, azimuth, values, shading="flat", rasterized=True, antialiased=False,
            cmap=cmap, vmin=limits[0], vmax=limits[1],
        )
        ax.set(xlim=(-6.55, 6.55), ylim=(0, 360), yticks=[0, 90, 180, 270, 360])
        ax.tick_params(axis="x", pad=6)
        ax.set_xticks(phase_ticks, labels=[r"$-2\pi$", r"$-\pi$", "0", r"$\pi$", r"$2\pi$"])

    fig.supxlabel("Phase (rad)", x=0.4795, y=0.038, fontsize=15)
    fig.supylabel(r"Azimuth ($\degree$)", x=0.013, y=0.540, fontsize=15)
    save(fig, image, name, label, ticks)


if __name__ == "__main__":
    with np.load(folder / "data.npz", allow_pickle=False) as data:
        spatial(data, "amp", r"$m=1$ amplitude", "magma", (0, 500), [0, 100, 200, 300, 400, 500])
        spatial(data, "phase", r"$m=1$ phase (rad)", "twilight", (-np.pi, np.pi), [-np.pi, 0, np.pi], [r"$-\pi$", "0", r"$\pi$"])
        spatial(data, "amp_rms", "Amplitude RMS", "magma", (0, 30), [0, 10, 20, 30])
        spatial(data, "phase_rms", "Phase RMS (rad)", "magma", (0, 2.5), [0, 0.5, 1, 1.5, 2, 2.5])
        cd_map(data, "cd", "CD (%)", "RdBu_r", (-30, 30), [-30, -15, 0, 15, 30])
        cd_map(data, "cd_rms", "CD RMS", "magma", (0, 7), [0, 2, 4, 6])
