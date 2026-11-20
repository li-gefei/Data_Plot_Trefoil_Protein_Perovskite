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
    "svg.hashsalt": "Film_Perovskite",
})


def position_labels(axes, labels):
    for ax, label in zip(axes, labels):
        ax.annotate(
            label, (0.5, 1), xycoords="axes fraction", xytext=(0, 7),
            textcoords="offset points", ha="center", va="bottom", fontsize=15,
        )


def save(fig, image, name, label, ticks, tick_labels=None):
    color_ax = fig.add_axes((0.915, 0.24, 0.014, 0.57))
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
    fig, axes = plt.subplots(2, 4, figsize=(12.8, 6.15), sharex=True, sharey=True)
    fig.subplots_adjust(left=0.106, right=0.895, bottom=0.120, top=0.938, wspace=0.105, hspace=0.13)
    extent = data["extent"]
    position_labels(axes[0], data["position"])

    for row, maps, side in zip(axes, data[name], data["side"]):
        for ax, values in zip(row, maps):
            image = ax.imshow(
                values, extent=extent, origin="upper", interpolation="nearest",
                cmap=cmap, vmin=limits[0], vmax=limits[1],
            )
            ax.set(xticks=[300, 500, 700], yticks=[300, 500, 700])
        box = row[0].get_position()
        fig.text(0.052, box.y0 + box.height / 2, side, ha="center", va="center", fontsize=16, fontweight="bold")

    fig.supxlabel("Pixel", x=0.5005, y=0.030, fontsize=15)
    fig.supylabel("Pixel", x=0.016, y=0.529, fontsize=15)
    save(fig, image, name, label, ticks, tick_labels)


def cd_map(data, name, label, cmap, limits, ticks):
    fig, axes = plt.subplots(1, 4, figsize=(12.8, 3.65), sharex=True, sharey=True)
    fig.subplots_adjust(left=0.080, right=0.895, bottom=0.232, top=0.870, wspace=0.200)
    phase = data["cd_phase"]
    azimuth = data["azimuth"]
    phase_ticks = [-2 * np.pi, -np.pi, 0, np.pi, 2 * np.pi]
    position_labels(axes, data["position"])

    for ax, values in zip(axes, data[name]):
        image = ax.pcolormesh(
            phase, azimuth, values, shading="flat", edgecolors="face", linewidth=.06,
            cmap=cmap, vmin=limits[0], vmax=limits[1],
        )
        ax.set(
            xlim=(-2 * np.pi, 2 * np.pi), ylim=(0, 360),
            yticks=[0, 90, 180, 270, 360],
        )
        ax.set_xticks(phase_ticks, labels=[r"$-2\pi$", r"$-\pi$", "0", r"$\pi$", r"$2\pi$"])

    axes[0].set_ylabel(r"Azimuth ($\degree$)", fontsize=15)
    fig.supxlabel("Phase (rad)", x=0.4875, y=0.050, fontsize=15)
    save(fig, image, name, label, ticks)


if __name__ == "__main__":
    with np.load(folder / "data.npz", allow_pickle=False) as data:
        spatial(data, "amp", r"$m=1$ amplitude", "magma", (0, 6), [0, 2, 4, 6])
        spatial(data, "phase", r"$m=1$ phase (rad)", "twilight", (-np.pi, np.pi), [-np.pi, 0, np.pi], [r"$-\pi$", "0", r"$\pi$"])
        spatial(data, "amp_rms", "Amplitude RMS", "magma", (0, 1.2), [0, 0.4, 0.8, 1.2])
        spatial(data, "phase_rms", "Phase RMS (rad)", "magma", (0, 2.5), [0, 0.5, 1, 1.5, 2, 2.5])
        cd_map(data, "cd", "CD (%)", "RdBu_r", (-6, 6), [-6, -3, 0, 3, 6])
        cd_map(data, "cd_rms", "CD RMS", "magma", (0, 3.5), [0, 1, 2, 3, 3.5])
