"""Visualization of distributions."""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_counts(data, columns=None, sup_title=None, fillna=True, max_cardinality=25):
    """Plot counts of categorical columns.
    
    Args:
        data (pd.DataFrame): data to plot.
        columns (list): columns to plot.
        sup_title (str): super title of the plot.
        fillna (bool): fill missing values with 'NaN'.
        max_cardinality (int): maximum cardinality of columns to plot.
    """
    data = data.copy()

    # fill missing categories
    if fillna:
        data = data.fillna('NaN').replace('', 'NaN')

    if columns is None:
        columns = data.columns
    
    # filter columns with high cardinality
    if max_cardinality:
        # remove columns that exceed max cardinality
        column_cardinality = data.nunique()

         # warn user that columns won't be displayed
        high_cardinality_cols = column_cardinality[column_cardinality > max_cardinality]
        if high_cardinality_cols.any():
            print(f"Columns with cardinality > {max_cardinality} will not be displayed:\n{high_cardinality_cols} ")
        
        # keep remaining columns
        columns = [col for col in columns if col not in high_cardinality_cols]
    

    if len(columns) == 0:
        print("No columns to plot")
        return None
    
    print(f"Plotting counts for columns: {columns}")

    # plot counts per column
    fig, ax = plt.subplots(1, len(columns), figsize=(20, 5))
    for i, col in enumerate(columns):
        ax_i = ax[i] if len(columns) > 1 else ax
        sns.countplot(data=data, x=col, ax=ax_i)

        # rotating x-axis labels for better readability
        ax_i.tick_params(axis='x', labelrotation = 45)

    if sup_title:
        fig.suptitle(sup_title)



    plt.show()
    return ax