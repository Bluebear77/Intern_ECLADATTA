
import pandas as pd
import matplotlib.pyplot as plt
from upsetplot import UpSet, from_contents
import warnings

# Suppress future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# List of dataset filenames
datasets = [
    "F2WTQ.csv", "FeTaQA.csv", "LOGICNLG.csv", "LOTNLG.csv", "ToTTo.csv",
    "WTQ.csv", "business100.csv", "female100.csv", "telco100.csv"
]

# Dictionary to store URLs from each dataset
url_dict = {}

# Load datasets and extract URLs
for dataset in datasets:
    df = pd.read_csv(dataset)
    url_dict[dataset] = set(df.iloc[:, 0])

# Prepare data for the UpSet plot
contents = {name: list(urls) for name, urls in url_dict.items()}

# Create an UpSet plot
upset_data = from_contents(contents)
upset = UpSet(upset_data)

# Plot the UpSet plot
upset.plot()
plt.suptitle('URL Overlap Across Datasets')

# Save the plot as a PNG file
plt.savefig('upset_plot.png', dpi=300)
