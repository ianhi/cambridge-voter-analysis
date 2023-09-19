from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def multi_year_bar(
    df: pd.DataFrame,
    bar_function,
    years=None,
    years_per_row: int = 3,
    figsize=(16, 6),
    sharex=True,
    sharey=True,
    **kwargs,
):
    """
    df : pd.DataFrame
        Expected to have "years" as the first level of index
        Additionally should have been passed through *turnout_year_key*
    bar_function : Callable
        Function accepting (df, year, ax=ax) and populating a bar graph
    years : arraylike, optional
        The years to make plots for. Default *None* will make for all years
        in the dataframe.
    years_per_row : int
        How many year plots to put on one year
    figsize, sharex, sharey:
        Passed on *plt.subplots*
    **kwargs :
        Passed to *bar_function*

    Returns
    -------
    fig
    axs
    """
    if years is None:
        years = sorted(df.index.unique(level=0))[::-1]
    nrows = np.ceil(len(years) / years_per_row).astype(int)
    fig, axs = plt.subplots(
        nrows, years_per_row, figsize=figsize, sharex=sharex, sharey=sharey
    )

    flat_ax = axs.reshape(-1)
    for i, year in enumerate(years):
        ax = flat_ax[i]
        ax.set_title(f"{year}")
        bar_function(df, year, ax=ax, **kwargs)

    # now hide any unused axes
    for i in range(len(years), nrows * years_per_row):
        flat_ax[i].axis("off")
    return fig, axs


def turnout_bar_graph(df, year, ax=None, bar_width=3.75):
    if ax is None:
        ax = plt.gca()
    ax.bar(
        df.loc[year]["mid_points"],
        df.loc[year]["registered"],
        width=bar_width,
        color="gray",
        label="Registered - did not vote",
    )
    ax.bar(
        df.loc[year]["mid_points"],
        df.loc[year]["voted"],
        width=bar_width,
        color="tab:green",
        label="Voted",
    )


def university_housing_bar_chart(
    df,
    year,
    idx,
    ax,
    bar_width=0.75,
):
    registered = df[idx].loc[year]["univ_housing_name"].value_counts().sort_index()
    voted = (
        df[idx]
        .loc[year]
        .groupby("univ_housing_name")
        .sum(numeric_only=True)
        .sort_index()
    )
    sort_idx = voted["voted"].argsort()[::-1]
    voted = voted.iloc[sort_idx]
    registered = registered.iloc[sort_idx]
    ax.bar(
        registered.index,
        registered,
        width=bar_width,
        color="gray",
        label="Registered - did not vote",
    )
    ax.bar(
        voted.index, voted["voted"], width=bar_width, color="tab:green", label="Voted"
    )
    ax.set_title(f"{year}")
    # adjust the names to drop the suffixes that are in there.

    ax.tick_params(axis="x", labelrotation=90)
