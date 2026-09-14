"""Shared plotting utilities for the Galactic Dynamics course."""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
from matplotlib.figure import Figure


TEXTWIDTH_PT = 469.75502
DOCUMENT_FONT_SIZE_PT = 10.0

TEX_POINTS_PER_INCH = 72.27
INCHES_PER_TEX_POINT = 1.0 / TEX_POINTS_PER_INCH


def set_latex_style(
    font_size: float = DOCUMENT_FONT_SIZE_PT,
    *,
    use_tex: bool = True,
    latex_preamble: tuple[str, ...] = (),
) -> None:
    """Configure Matplotlib to match the lecture-note typography.

    Parameters
    ----------
    font_size
        Base font size in TeX points.
    use_tex
        Whether Matplotlib should use LaTeX to render text.
    latex_preamble
        Additional commands to include in Matplotlib's LaTeX preamble.
    """
    if font_size <= 0:
        raise ValueError("font_size must be positive.")

    # Matplotlib font sizes are expressed in PostScript points
    # (72 pt/in), whereas LaTeX uses TeX points (72.27 pt/in).
    mpl_font_size = font_size * 72.0 / TEX_POINTS_PER_INCH

    mpl.rcParams.update(
        {
            "text.usetex": use_tex,

            "font.family": "serif",
            "font.size": mpl_font_size,

            # Axes
            "axes.labelsize": mpl_font_size,
            "axes.titlesize": mpl_font_size,
            "axes.labelweight": "normal",
            "axes.titleweight": "normal",

            # Tick labels
            "xtick.labelsize": mpl_font_size,
            "ytick.labelsize": mpl_font_size,

            # Legends
            "legend.fontsize": mpl_font_size,
            "legend.title_fontsize": mpl_font_size,

            # Figure-level text
            "figure.titlesize": mpl_font_size,
            "figure.labelsize": mpl_font_size,

            # General drawing settings
            "axes.linewidth": 0.8,
            "lines.linewidth": 1.2,
            "xtick.direction": "out",
            "ytick.direction": "out",
            "savefig.dpi": 300,
        }
    )

    # Always reset the preamble, including when the tuple is empty.
    mpl.rcParams["text.latex.preamble"] = "\n".join(latex_preamble)


def latex_figsize(
    fraction: float = 1.0,
    *,
    width_pt: float = TEXTWIDTH_PT,
    height_ratio: float = 0.62,
) -> tuple[float, float]:
    """Return a figure size matching a fraction of a LaTeX width.

    Parameters
    ----------
    fraction
        Fraction of ``width_pt`` occupied by the figure in the LaTeX file.
    width_pt
        Available LaTeX width in TeX points. By default, this is the
        lecture notes' ``\\textwidth``.
    height_ratio
        Figure height divided by figure width.

    Returns
    -------
    tuple[float, float]
        Figure width and height in inches.
    """
    if width_pt <= 0:
        raise ValueError("width_pt must be positive.")

    if not 0 < fraction <= 1:
        raise ValueError("fraction must lie in the interval (0, 1].")

    if height_ratio <= 0:
        raise ValueError("height_ratio must be positive.")

    width_in = width_pt * fraction * INCHES_PER_TEX_POINT
    height_in = width_in * height_ratio

    return width_in, height_in


def save_figure(
    fig: Figure,
    output: str | Path,
    *,
    save_pdf: bool = False,
    save_png: bool = False,
    png_dpi: int = 300,
) -> None:
    """Save a figure without changing its physical dimensions.

    ``bbox_inches='tight'`` is deliberately avoided because it changes the
    exported bounding box. That would cause LaTeX to rescale the figure and
    alter the effective font size.
    """
    if png_dpi <= 0:
        raise ValueError("png_dpi must be positive.")

    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    stem = output.with_suffix("")

    if save_pdf:
        fig.savefig(stem.with_suffix(".pdf"))

    if save_png:
        fig.savefig(stem.with_suffix(".png"), dpi=png_dpi)