import numpy as np 
import pandas as pd
frame = pd.DataFrame(np.arange(16).reshape((4,4)),
         index = ['red', 'blue', 'yellow', 'white'],
         columns = ['ball', 'pen', 'pencil', 'paper'])
frame.to_csv('ch05_07.csv')