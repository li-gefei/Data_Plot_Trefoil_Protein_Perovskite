from pathlib import Path

import matplotlib as mpl
import numpy as np

mpl.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


folder = Path(__file__).resolve().parent
ticks = [0, 2*np.pi, 4*np.pi, 6*np.pi, 8*np.pi, 10*np.pi, 12*np.pi, 14*np.pi, 15*np.pi]
labels = ["0", r"$2\pi$", r"$4\pi$", r"$6\pi$", r"$8\pi$", r"$10\pi$", r"$12\pi$", r"$14\pi$", r"$15\pi$"]
mpl.rcParams.update({
    "font.family": "Arial",
    "mathtext.fontset": "custom",
    "mathtext.rm": "Arial",
    "mathtext.it": "Arial:italic",
    "mathtext.fallback": None,
    "font.size": 13,
    "axes.labelsize": 15,
    "axes.linewidth": 1.0,
    "axes.spines.top": True,
    "axes.spines.right": True,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.top": True,
    "ytick.right": True,
    "svg.fonttype": "none",
    "svg.hashsalt": "Wedge_Drift_Phase",
})


def save(fig, name):
    fig.savefig(folder / f"{name}.svg", dpi=300, metadata={"Date": None, "Creator": None})
    plt.close(fig)


def mapping(data, side, index):
    fig = plt.figure(figsize=(9.7, 7.9))
    top = fig.add_axes((.103, .537, .865, .416))
    bottom = fig.add_axes((.103, .121, .865, .416), sharex=top)
    for ax, key, edge in ((top, "fit", "fit_edges"), (bottom, "measured", "measured_edges")):
        image = ax.pcolormesh(
            data[edge], data["round_edges"], data[key][index], cmap="magma",
            vmin=0, vmax=1, shading="flat", edgecolors="face",
        )
        ax.set(
            xlim=data["phase_limits"], ylim=(.5, 10.5), ylabel="Round",
            yticks=range(1, 11), xticks=ticks, xticklabels=labels,
        )
        ax.tick_params(pad=6)
        for spine in ax.spines.values():
            spine.set_zorder(20)
    top.tick_params(axis="x", bottom=False, labelbottom=False)
    bottom.tick_params(axis="x", top=False)
    bottom.set_xlabel("Phase (rad)", labelpad=7)

    top.add_patch(Rectangle(
        (.681, .710), .297, .260, transform=top.transAxes,
        facecolor="white", edgecolor="none", alpha=.8, zorder=30,
    ))
    axis = top.inset_axes([.71, .80, .235, .04], zorder=31)
    bar = fig.colorbar(image, cax=axis, orientation="horizontal", ticks=[0, .5, 1])
    bar.solids.set_rasterized(False)
    bar.solids.set_edgecolor("face")
    bar.solids.set_linewidth(.06)
    bar.set_ticks([0, .5, 1], labels=["0", "0.5", "1"])
    bar.set_label("Normalized THG integral", labelpad=6)
    axis.xaxis.set_label_position("top")
    axis.tick_params(top=False, pad=4)
    save(fig, side)


def comparison(data):
    fig = plt.figure(figsize=(9.7, 5.15))
    ax = fig.add_axes((.120, .171, .848, .772))
    phase = data["phase"]
    error_phase = data["error_phase"]
    for i, (side, color) in enumerate((("L", "#2D518A"), ("R", "#D9533D"))):
        ax.fill_between(phase, data["low"][i], data["high"][i], color=color, alpha=.16, linewidth=0, zorder=1)
        ax.plot(phase, data["mean"][i], color=color, linewidth=1.8, label=side, solid_capstyle="round", zorder=4)
        ax.errorbar(
            error_phase, data["error_mean"][i], yerr=data["error_sd"][i],
            fmt="none", ecolor=color, elinewidth=.8, capsize=2.4, capthick=.8, alpha=.85, zorder=3,
        )
    ax.set(
        xlim=data["phase_limits"], ylim=data["lr_ylim"], xticks=ticks, xticklabels=labels,
        yticks=[0, .25, .50, .75, 1], xlabel="Phase (rad)", ylabel="Normalized THG integral",
    )
    ax.tick_params(pad=6)
    ax.legend(loc="upper right", ncols=2, frameon=False, handlelength=2.2, columnspacing=1.6)
    save(fig, "LR")


if __name__ == "__main__":
    with np.load(folder / "data.npz", allow_pickle=False) as data:
        mapping(data, "L", 0)
        mapping(data, "R", 1)
        comparison(data)
