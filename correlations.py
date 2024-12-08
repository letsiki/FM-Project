import pandas as pd
from scipy.stats import spearmanr
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def calculate_correlations(df, negative_stat=False):

    # Check if there are enough rows
    if len(df) < 30:
        print("Not enough data for a statistically safe calculation. At least 30 rows are recommended.")
        return
    
    # Initialize an empty dictionary to store correlation values
    correlations = {}
    df = df.dropna()
    # I coukd be using standardization and PCA to detect attributes that influence each other 

    # Calculate the correlation of the second column with each column from the fifth to the end
    for col in df.columns[4:]:
        # correlations[col] = df.iloc[:, 3].corr(df[col])
        corr, p_value = spearmanr(df.iloc[:, 3], df[col])
        if p_value < 0.05:  # Default Value if p-value is 0.05
            correlations[col] = corr
    
    # Sort the correlations dictionary by value in descending order
    if not negative_stat:
        sorted_correlations = sorted(correlations.items(), key=lambda x: x[1], reverse=True)
    else:
        sorted_correlations = sorted(correlations.items(), key=lambda x: x[1], reverse=False)
    
    # Print Label
    print(f'Correlation of player attributes with {df.columns[3]}:\n')
    # Print the sorted correlations
    for col, corr in sorted_correlations:
        print(f"{col}: {corr:.2f}")

    return dict(sorted_correlations)

# Example usage
# df = pd.read_csv('your_dataframe.csv')
# feature_importances = analyze_player_attributes(df)
# print(feature_importances)
