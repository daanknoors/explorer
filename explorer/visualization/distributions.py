"""Visualization of distributions."""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from explorer.visualization import format


def plot_counts(data, columns=None, fillna=True, top_n=25, hue=None, title=None):
    """Plot top counts of categorical columns, group remaining into 'Other'.
    
    Args:
        data (pd.DataFrame): data to plot.
        columns (list): columns to plot.
        fillna (bool): fill missing values with 'NaN'.
        top_n (int): number of top categories to display.
    """
    data = data.copy()

    # fill missing categories
    if fillna:
        data = data.fillna('NaN').replace('', 'NaN')

    if columns is None:
        columns = data.columns
    elif isinstance(columns, str):
        columns = [columns]
    else:
        raise ValueError("columns must be a list or a string")

    fig, ax = plt.subplots(len(columns), 1, figsize=(6, 8*len(columns)))
    for i, col in enumerate(columns):
        top_categories = data[col].value_counts().index[:top_n].to_list()
        # group remaining categories to other
        data[col] = data[col].apply(lambda x: x if x in top_categories else 'Other')

        # plot counts
        ax_i = ax[i] if len(columns) > 1 else ax
        sns.countplot(data=data, y=col, hue=hue, ax=ax_i, dodge=False, order=top_categories + ['Other'], color=format.PALETTE_BLUE[2])

        # rotating x-axis labels for better readability
        ax_i.tick_params(axis='x', labelrotation=45)

        if i == 0:
            title = title or "Counts per column"
            ax_i.set_title(f"{title}")
        ax_i.set_xlabel('')

    sns.despine()
    plt.tight_layout()
    plt.show()
    return ax


