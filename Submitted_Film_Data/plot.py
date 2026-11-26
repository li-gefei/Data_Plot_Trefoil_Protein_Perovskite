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
    "svg.hashsalt": "Submitted_Film_Data",
})


def save(fig, name):
    fig.savefig(folder / f"{name}.svg", dpi=300, metadata={"Date": None, "Creator": None})
    plt.close(fig)


def scale(fig, image, title, ticks, labels=None):
    ax = fig.add_axes((.875, .24, .016, .55))
    bar = fig.colorbar(image, cax=ax, ticks=ticks)
    if labels is not None:
        bar.set_ticks(ticks, labels=labels)
    bar.set_label(title, labelpad=8)


def camera_map(values, name, title, cmap, vmax, ticks, labels=None, vmin=0):
    fig, axes = plt.subplots(1, 2, figsize=(8.3, 3.75))
    fig.subplots_adjust(left=.105, right=.845, bottom=.20, top=.86, wspace=.30)
    for ax, sample, image_data in zip(axes, ("S", "R"), values):
        image = ax.imshow(image_data, origin="lower", interpolation="none",
                          cmap=cmap, vmin=vmin, vmax=vmax)
        ax.set_title(f"{sample}-Perovskite", fontsize=15)
        ax.set_xlabel("Pixel")
        ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(100))
        ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(100))
        ax.tick_params(labelbottom=False, labelleft=False)
    axes[0].set_ylabel("Pixel")
    scale(fig, image, title, ticks, labels)
    save(fig, name)


def cd(d):
    fig, ax = plt.subplots(figsize=(5.45, 3.75))
    fig.subplots_adjust(left=.175, right=.755, bottom=.20, top=.94)
    image = ax.pcolormesh(d["phase_rad"], d["azimuth_deg"], d["value"], shading="gouraud",
                          cmap="RdBu_r", vmin=-1, vmax=1, rasterized=True)
    ax.set(xlabel="Phase (rad)", ylabel="Azimuth (°)", yticks=[0, 90, 180, 270, 360])
    ax.set_xticks([0, np.pi, 2*np.pi, 3*np.pi], ["0", r"$\pi$", r"$2\pi$", r"$3\pi$"])
    bar = fig.colorbar(image, cax=fig.add_axes((.79, .25, .023, .60)), ticks=[-1, 0, 1])
    bar.set_label("Normalized CD")
    save(fig, "cd")


def trace(ax, d, key, quantity, color, label=None):
    tint = {"#3c5488": "#d9dde8", "#e64b35": "#f8e0db", "black": "#d9d9d9"}
    band = d[f"{key}_band"]
    curve = d[key]
    ax.fill(band["phase_rad"], band[quantity], facecolor=tint[color], edgecolor="none")
    ax.plot(curve["phase_rad"], curve[quantity], color=color, linewidth=2, label=label)


def spectrum(d):
    fig, (intensity, cd_axis) = plt.subplots(
        2, 1, sharex=True, figsize=(4.25, 5.1),
        gridspec_kw={"height_ratios": [1.45, 1]},
    )
    fig.subplots_adjust(left=.24, right=.96, bottom=.15, top=.89, hspace=.12)
    trace(intensity, d, "s", "intensity", "#3c5488", "S")
    trace(intensity, d, "r", "intensity", "#e64b35", "R")
    intensity.set(xlim=(0, 12), ylim=(6.89e7, 8.12e7),
                  ylabel="Intensity (arb. units)", title="S- and R-Perovskite")
    intensity.set_yticks([7e7, 7.5e7, 8e7], ["70M", "75M", "80M"])
    intensity.legend(loc="upper center", ncol=2, frameon=False, fontsize=10, handlelength=1.5)
    trace(cd_axis, d, "cd", "cd_percent", "black")
    cd_axis.set(ylim=(-6.7, 5.7), yticks=[-5, 0, 5], xlabel="Phase (rad)", ylabel="CD (%)")
    cd_axis.set_xticks([0, np.pi, 2*np.pi, 3*np.pi],
                       ["0", r"$\pi$", r"$2\pi$", r"$3\pi$"])
    save(fig, "spectrum")


if __name__ == "__main__":
    with np.load(folder / "data.npz", allow_pickle=False) as data:
        camera_map(data["amp"], "amp", r"$A_1$ / peak $A_1$", "magma", 1, [0, .5, 1])
        camera_map(data["amp_rms"], "amp_rms", "Amplitude RMS / peak", "magma",
                   .035, [0, .01, .02, .03])
        camera_map(data["phase"], "phase", r"$m=1$ phase (rad)", "twilight_shifted",
                   np.pi, [-np.pi, 0, np.pi], [r"$-\pi$", "0", r"$\pi$"], vmin=-np.pi)
        camera_map(data["phase_rms"], "phase_rms", "Phase RMS (rad)", "magma",
                   np.pi, [0, np.pi/2, np.pi], ["0", r"$\pi/2$", r"$\pi$"])
        cd(data["cd"])
        spectrum(data["spectrum"])
