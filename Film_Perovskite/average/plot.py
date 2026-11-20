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
    "axes.spines.bottom": True,
    "axes.spines.left": True,
    "svg.fonttype": "none",
    "svg.hashsalt": "Perovskite_average",
})


def save(fig, image, axis, name, label, ticks, tick_labels=None):
    color = fig.colorbar(image, cax=axis, ticks=ticks)
    color.solids.set_rasterized(False)
    color.solids.set_edgecolor("face")
    color.solids.set_linewidth(.06)
    if tick_labels is not None:
        color.set_ticks(ticks, labels=tick_labels)
    color.set_label(label, labelpad=9)
    fig.savefig(folder / f"{name}.svg", dpi=300, metadata={"Date": None, "Creator": None})
    plt.close(fig)


def spatial(data, name, label, cmap, limits, ticks, tick_labels=None):
    fig, axes = plt.subplots(2, 1, figsize=(5.65, 7.5), sharex=True, sharey=True)
    fig.subplots_adjust(left=.204, right=.774, bottom=.102, top=.974, hspace=.12)
    extent = data["extent"]
    palette = mpl.colormaps[cmap].with_extremes(bad="#e4e4e4")
    for ax, values, side in zip(axes, data[name], data["side"]):
        image = ax.imshow(
            values, extent=extent, origin="upper", interpolation="nearest",
            cmap=palette, vmin=limits[0], vmax=limits[1],
        )
        ax.set(xticks=data["pixel_x"], yticks=data["pixel_y"])
        box = ax.get_position()
        fig.text(.087, box.y0 + box.height / 2, side, ha="center", va="center", fontsize=16, fontweight="bold")

    fig.supxlabel("Pixel", x=.489, y=.027)
    fig.supylabel("Pixel", x=.022, y=.538)
    axis = fig.add_axes((.822, .255, .026, .55))
    save(fig, image, axis, name, label, ticks, tick_labels)


def cd_map(data, name, label, cmap, limits, ticks):
    fig = plt.figure(figsize=(6.65, 4.12))
    ax = fig.add_axes((.139, .213, .677, .722))
    axis = fig.add_axes((.857, .258, .024, .624))
    image = ax.pcolormesh(
        data["cd_phase"], data["azimuth"], data[name],
        cmap=cmap, vmin=limits[0], vmax=limits[1], shading="flat", edgecolors="face", linewidth=.06,
    )
    ax.set(
        xlim=data["cd_xlim"], ylim=(0, 360), yticks=[0, 90, 180, 270, 360],
        xlabel="Phase (rad)", ylabel=r"Azimuth ($\degree$)",
    )
    ax.tick_params(axis="x", pad=6)
    ax.set_xticks([-2*np.pi, -np.pi, 0, np.pi, 2*np.pi], labels=[r"$-2\pi$", r"$-\pi$", "0", r"$\pi$", r"$2\pi$"])
    save(fig, image, axis, name, label, ticks)


if __name__ == "__main__":
    with np.load(folder / "data.npz", allow_pickle=False) as data:
        amp_max, amp_rms_max, cd_max, cd_rms_max = data["scale_max"]
        spatial(data, "amp", r"$m=1$ amplitude", "magma", (0, amp_max), data["amp_ticks"])
        spatial(data, "phase", r"$m=1$ phase (rad)", "twilight", (-np.pi, np.pi), [-np.pi, 0, np.pi], [r"$-\pi$", "0", r"$\pi$"])
        spatial(data, "amp_rms", "Amplitude RMS", "magma", (0, amp_rms_max), data["amp_rms_ticks"])
        phase_rms_ticks = data["phase_rms_ticks"]
        spatial(data, "phase_rms", "Phase RMS (rad)", "magma", (0, phase_rms_ticks[-1]), phase_rms_ticks)
        cd_map(data, "cd", "CD (%)", "RdBu_r", (-cd_max, cd_max), [-cd_max, -cd_max/2, 0, cd_max/2, cd_max])
        cd_map(data, "cd_rms", "CD RMS", "magma", (0, cd_rms_max), data["cd_rms_ticks"])
