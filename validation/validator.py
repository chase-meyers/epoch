import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def validate(df_features, regimes):
    validation_df = df_features.copy()
    validation_df['regime'] = regimes
    validation_df = validation_df.dropna()
    grouping_validation_df = validation_df.groupby('regime').agg({
        'returns': ['mean', 'std', 'count'],
        'volatility': ['mean', 'std'],
        'momentum': ['mean', 'std']
    })
    
    return grouping_validation_df, validation_df

def generate_charts(data, validation_df):
    spans = pd.DataFrame({
        'start': validation_df.index[validation_df['regime'].diff() != 0],
        'end': validation_df.index[validation_df['regime'].diff() != 0][1:].append(pd.Index([validation_df.index[-1]])),
        'regime': validation_df['regime'][validation_df['regime'].diff() != 0].values
    })

    fig, axes = plt.subplots(2, 2, figsize=(30, 14))
    
    
    # Full period regime chart
    data['Close'].plot(ax=axes[0, 0], color='black', label='Close Price')
    for _, row in spans.iterrows():
        if row['regime'] == 0:
            axes[0, 0].axvspan(row['start'], row['end'], color='orange', alpha=0.3)
        elif row['regime'] == 1:
            axes[0, 0].axvspan(row['start'], row['end'], color='yellow', alpha=0.3)
        elif row['regime'] == 2:
            axes[0, 0].axvspan(row['start'], row['end'], color='red', alpha=0.3)
        elif row['regime'] == 3:
            axes[0, 0].axvspan(row['start'], row['end'], color='green', alpha=0.3)


    # One year regime chart
    recent_data = data.tail(252)
    recent_validation = validation_df.tail(252)

    recent_data['Close'].plot(ax=axes[0, 1], color='black', label='Close Price Recent')
    for _, row in spans.iterrows():
        if row['regime'] == 0 and row['start'] >= recent_validation.index[0]:
            axes[0, 1].axvspan(row['start'], row['end'], color='orange', alpha=0.3)
        elif row['regime'] == 1 and row['start'] >= recent_validation.index[0]:
            axes[0, 1].axvspan(row['start'], row['end'], color='yellow', alpha=0.3)
        elif row['regime'] == 2 and row['start'] >= recent_validation.index[0]:
            axes[0, 1].axvspan(row['start'], row['end'], color='red', alpha=0.3)
        elif row['regime'] == 3 and row['start'] >= recent_validation.index[0]:
            axes[0, 1].axvspan(row['start'], row['end'], color='green', alpha=0.3)


    # 2008 crisis regime chart
    data_2008 = data['2007-01-01':'2009-12-31']
    validation_2008 = validation_df['2007-01-01':'2009-12-31']

    data_2008['Close'].plot(ax=axes[1, 0], color='black', label='Close Price 2008')
    for _, row in spans.iterrows():
        if row['regime'] == 0 and row['start'] >= validation_2008.index[0] and row['end'] <= validation_2008.index[-1]:
            axes[1, 0].axvspan(row['start'], row['end'], color='orange', alpha=0.3)
        elif row['regime'] == 1 and row['start'] >= validation_2008.index[0] and row['end'] <= validation_2008.index[-1]:
            axes[1, 0].axvspan(row['start'], row['end'], color='yellow', alpha=0.3)
        elif row['regime'] == 2 and row['start'] >= validation_2008.index[0] and row['end'] <= validation_2008.index[-1]:
            axes[1, 0].axvspan(row['start'], row['end'], color='red', alpha=0.3)
        elif row['regime'] == 3 and row['start'] >= validation_2008.index[0] and row['end'] <= validation_2008.index[-1]:
            axes[1, 0].axvspan(row['start'], row['end'], color='green', alpha=0.3)



    # 2020 crisis regime chart
    data_2020 = data['2020-01-01':'2021-12-31']
    data_2020['Close'].plot(ax=axes[1, 1], color='black', label='Close Price 2020')
    for _, row in spans.iterrows():
        if row['regime'] == 0 and row['start'] >= data_2020.index[0] and row['end'] <= data_2020.index[-1]:
            axes[1, 1].axvspan(row['start'], row['end'], color='orange', alpha=0.3)
        elif row['regime'] == 1 and row['start'] >= data_2020.index[0] and row['end'] <= data_2020.index[-1]:
            axes[1, 1].axvspan(row['start'], row['end'], color='yellow', alpha=0.3)
        elif row['regime'] == 2 and row['start'] >= data_2020.index[0] and row['end'] <= data_2020.index[-1]:
            axes[1, 1].axvspan(row['start'], row['end'], color='red', alpha=0.3)
        elif row['regime'] == 3 and row['start'] >= data_2020.index[0] and row['end'] <= data_2020.index[-1]:
            axes[1, 1].axvspan(row['start'], row['end'], color='green', alpha=0.3)

    legend_elements = [
        mpatches.Patch(facecolor='green', alpha=0.3, label='Bull/Trending'),
        mpatches.Patch(facecolor='yellow', alpha=0.3, label='Sideways/Neutral'),
        mpatches.Patch(facecolor='orange', alpha=0.3, label='High Volatility'),
        mpatches.Patch(facecolor='red', alpha=0.3, label='Crisis/Bear')
    ]

    fig.legend(handles=legend_elements, loc='lower center', ncol=4, bbox_to_anchor=(0.5, -0.02))

    for ax in axes.flat:
        ax.set_xlabel('')

    fig.suptitle('EPOCH — Market Regime Analysis', fontsize=16, fontweight='bold', y=1.01)

    axes[0, 0].set_title('Full History Regimes (2000-Present)')
    axes[0, 1].set_title('Recent Market Regimes (Past Year)')
    axes[1, 0].set_title('2008 Financial Crisis Validation')
    axes[1, 1].set_title('2020 COVID Crash Validation')

    chart_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'outputs', 'charts', 'regime_overlay.png')
    plt.savefig(chart_path, dpi=150, bbox_inches='tight')
    plt.close()
    print("Analysis complete. Charts saved to outputs/charts/")
    
    show_chart = str(input("Open charts? (y/n): "))
    if show_chart.lower() == 'y':
        os.startfile(chart_path)
    else:
        print("Charts not opened.")
        exit()