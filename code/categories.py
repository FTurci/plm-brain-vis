import numpy as np
import pandas as pd

labels = pd.read_table("../data/ROIname.txt").values
# clean labels
labs = [s[0].strip(""""'" """) for s in labels]
print(labs)
unique = np.unique(labs)
print(unique, len(labs), len(unique))