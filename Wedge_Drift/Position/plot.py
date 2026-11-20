from pathlib import Path

import matplotlib as mpl
import numpy as np

mpl.use("Agg")

import matplotlib.pyplot as plt


folder = Path(__file__).resolve().parent
leg_style = (("out", "#2868B2", "o"), ("back", "#D54445", "^"))
mpl.rcParams.update({
    "font.family": "Arial",
    "mathtext.fontset": "custom",
    "mathtext.rm": "Arial",
    "mathtext.it": "Arial:italic",
    "mathtext.fallback": None,
    "font.size": 13,
    "axes.labelsize": 15,
    "axes.linewidth": .9,
    "axes.spines.top": True,
    "axes.spines.right": True,
    "axes.edgecolor": "#353B40",
    "svg.fonttype": "none",
    "svg.hashsalt": "Wedge_Drift_Position",
    "path.simplify": False,
})


def draw(data):
    fig = plt.figure(figsize=(10.25, 6.35))
    grid = fig.add_gridspec(
        3, 1, left=.109, right=.967, bottom=.146, top=.940,
        hspace=0, height_ratios=(.8, 1, 1),
    )
    top = fig.add_subplot(grid[0])
    axes = [top, fig.add_subplot(grid[1], sharex=top), fig.add_subplot(grid[2], sharex=top)]
    for leg, color, marker in leg_style:
        top.plot(*data[f"stage_{leg}"], color=color, linewidth=.9)
    top.set(ylabel="Phase (rad)", yticks=data["stage_yticks"])
    band_extents = data["band_extent"]
    shift_ticks = data["shift_yticks"]
    rms_labels = data["rms_labels"]
    for index, (ax, direction) in enumerate(zip(axes[1:], "xy")):
        for j in range(10*index, 10*(index+1)):
            ax.imshow(data[f"band_{j}"], extent=band_extents[j], origin="lower", aspect="auto", interpolation="bilinear", zorder=0)
        for leg, color, marker in leg_style:
            frames = data[f"frames_{leg}"]
            ax.scatter(
                frames[0], frames[index+1], color=color, marker=marker, s=7.5,
                alpha=.45, edgecolors="none", zorder=2,
            )
        ax.set(ylabel=rf"$\Delta {direction}$ ($\mathrm{{\mu m}}$)", yticks=shift_ticks)
        ax.text(
            .977, .97, rms_labels[index], transform=ax.transAxes, ha="right", va="top",
            fontsize=13, zorder=6, bbox={"facecolor": "white", "edgecolor": "none", "alpha": .82, "pad": 2},
        )
    for i, (ax, ylim) in enumerate(zip(axes, data["ylim"])):
        ax.set(xlim=data["xlim"], ylim=ylim)
        ax.set_xticks(data["xticks"], labels=data["phase_labels"])
        if i < 2:
            ax.tick_params(axis="x", bottom=False, labelbottom=False)
    axes[-1].set_xlabel("Phase (rad)")
    return fig


if __name__ == "__main__":
    with np.load(folder / "data.npz", allow_pickle=False) as data:
        fig = draw(data)
        fig.savefig(folder / "position.svg", dpi=300, metadata={"Date": None, "Creator": None})
        plt.close(fig)
