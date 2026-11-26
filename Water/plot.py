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
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.linewidth": 0.95,
    "axes.spines.top": True,
    "axes.spines.right": True,
    "xtick.major.size": 3.4,
    "ytick.major.size": 3.4,
    "svg.fonttype": "none",
    "svg.hashsalt": "Water",
})


def figure(data):
    fig = plt.figure(figsize=(7.4, 5.65))
    grid = fig.add_gridspec(
        2, 3, left=0.13, right=0.9, bottom=0.112, top=0.928,
        width_ratios=(1, 1, 0.068), height_ratios=(1.22, 1), wspace=0.23, hspace=0.47,
    )
    beams = [fig.add_subplot(grid[0, 0]), fig.add_subplot(grid[0, 1])]
    traces = [fig.add_subplot(grid[1, 0]), fig.add_subplot(grid[1, 1])]
    for index, (beam, trace, color) in enumerate(zip(beams, traces, ("#2C6C9C", "#BD3E4A"), strict=True)):
        image = beam.imshow(
            data["beam"][index], extent=data["extent"], origin="upper",
            cmap="magma", vmin=0, vmax=1, interpolation="none",
        )
        beam.set_title(data["side"][index], fontsize=14, pad=6)
        beam.set(xticks=[600, 700, 800, 900], yticks=[500, 600, 700],
                 xlabel="X (px)", xlim=data["extent"][:2], ylim=data["extent"][2:])
        phase = data["phase"]
        trace.fill_between(phase, data["lower"][index], data["upper"][index], color=color,
                           alpha=0.13, linewidth=0)
        for values in data["trace"][index]:
            trace.plot(phase, values, color=color, alpha=0.28, linewidth=0.75)
        trace.plot(phase, data["mean"][index], color=color, linewidth=1.75)
        trace.set(xlim=(phase[0], phase[-1]), ylim=(0.5, 1.5),
                  yticks=[0.6, 0.8, 1, 1.2, 1.4], xlabel="Phase (rad)")
        trace.set_xticks(
            data["phase_ticks"],
            labels=[r"$-2\pi$", r"$-\pi$", "0", r"$\pi$", r"$2\pi$"],
        )
    beams[0].set_ylabel("Y (px)")
    beams[1].tick_params(labelleft=False)
    traces[0].set_ylabel("Normalized Intensity (arb. unit)", labelpad=8)
    traces[1].tick_params(labelleft=False)
    colorbar_axis = fig.add_subplot(grid[0, 2])
    colorbar = fig.colorbar(image, cax=colorbar_axis, ticks=[0, 0.25, 0.5, 0.75, 1])
    colorbar.set_label("Normalized Intensity", labelpad=7)
    return fig


if __name__ == "__main__":
    with np.load(folder / "data.npz", allow_pickle=False) as data:
        fig = figure(data)
    fig.savefig(folder / "water.svg", metadata={"Date": None, "Creator": None})
    plt.close(fig)
