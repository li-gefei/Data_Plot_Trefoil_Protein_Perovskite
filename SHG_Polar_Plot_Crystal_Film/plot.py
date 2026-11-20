from pathlib import Path

import matplotlib as mpl
import numpy as np

mpl.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def plot(data):
    mpl.rcParams.update({
        "font.family": "Arial",
        "font.size": 9,
        "svg.fonttype": "none",
        "svg.hashsalt": "perovskite-thg-20261118",
        "axes.linewidth": 0.7,
        "legend.frameon": False,
        "figure.facecolor": "none",
    })
    width, height = 210, 297
    fig = plt.figure(figsize=(width / 25.4, height / 25.4))
    ax = fig.add_axes(
        (69.380768 / width, 1 - 113.706249 / height, 90 / width, 90 / height),
        projection="polar",
        facecolor="white",
    )
    ax.set_theta_zero_location("E")
    ax.set_theta_direction(1)
    ax.set_thetagrids([0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330])
    ax.set_ylim(0, data["rmax"].item())
    ax.set_yticks([0.25, 0.50, 0.75, 1.00], labels=["0.25", "0.50", "0.75", "1.00"])
    ax.set_rlabel_position(90)
    ax.tick_params(axis="x", labelsize=9, pad=5, colors="black")
    ax.tick_params(axis="y", labelsize=8, colors="black")
    ax.grid(color="#D9DDE2", linewidth=0.5, linestyle=(0, (2, 2)))
    ax.spines["polar"].set_color("#A4ABB2")

    theta = data["theta"]
    points = data["theta_points"]
    handles = []
    for label, lower, upper, mean, color, marker in zip(
        data["labels"], data["lower"], data["upper"], data["mean"],
        ("#245F87", "#C67D38"), ("o", "s"),
    ):
        ax.fill_between(theta, lower, upper, color=color, alpha=0.23, lw=0, zorder=1)
        ax.scatter(points, mean, marker=marker, s=10, facecolors="white", edgecolors=color, linewidths=0.7, zorder=3)
        handles.append(Line2D(
            [], [], linestyle="none", marker=marker, ms=4, markerfacecolor="white",
            markeredgecolor=color, markeredgewidth=0.7, label=label,
        ))
    ax.legend(
        handles=handles, loc="upper center",
        bbox_to_anchor=(140.815683 / width, 1 - 15.73998 / height),
        bbox_transform=fig.transFigure, ncol=2, fontsize=9, columnspacing=1.8,
        handletextpad=0.5, borderaxespad=0,
    )
    return fig


if __name__ == "__main__":
    folder = Path(__file__).resolve().parent
    with np.load(folder / "data.npz", allow_pickle=False) as data:
        fig = plot(data)
        fig.savefig(folder / "shg.svg", metadata={"Date": None, "Creator": None})
        plt.close(fig)
