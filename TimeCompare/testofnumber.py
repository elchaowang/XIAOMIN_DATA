



import numpy as np
import pandas as pd

x = [0, np.NaN, 1.5, 5.2]

x = pd.DataFrame(x)

x = x.dropna()

x = x.astype(int)

print(x)











