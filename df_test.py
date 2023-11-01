# import module
import IPython
import pandas as pd
from IPython.display import display

PATH = "test-path.csv"
# assign dataframes
data1 = pd.DataFrame([[25, 77.5, 'A'], [30, 60.2, 'B'],
                      [25, 70.7, 'C']],
                     columns=['Students', 'Avg Marks', 'Section'])
data1.to_csv(PATH, encoding='utf-8')
data3 = pd.read_csv(PATH, encoding='utf-8', index_col=0)

data2 = pd.DataFrame([[30, 70.2, 'A'], [25, 65.2, 'B'],
                      [35, 77.7, 'C']],
                     columns=['Students', 'Avg Marks', 'Section'])


# display dataframes
print('Dataframes:')
display(data3)
display(data2)

# merge two data frames
print('After merging:')
display(pd.concat([data3, data2], axis=0))
