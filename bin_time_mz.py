import sys 
import pandas as pd
import numpy as np
import math
import glob

def bin_time(df, rt_window=10, mz_window=1.0005079):
    
    rt_dict = {}
    
    labels = [str(i) for i in range(1, rt_window+1)]
    
    df['RT_window'] = pd.qcut(df.sort_values(by='RT')['RT'].values, rt_window, labels=labels)
    
    for i in labels:
        
        test = df[df['RT_window'] == i].sort_values(by='MZ')
        
        binned_data = test.groupby(pd.cut(test['MZ'], bins = np.arange(0, 1801, mz_window)))['Intensity'].sum()
        
        rt_dict[i] = binned_data.values

    return np.array(list(rt_dict.values()))

if __name__ == '__main__':
    name = sys.argv[1].replace(".csv","")

    # use the line below if you're loading the features tsv file that has not had its first 0.05 and last 0.95 RT removed
    # df = pd.read_csv(sys.argv[1], delim_whitespace=True, header=None, skiprows=1, names=['RT', 'MZ', 'Intensity'])

    # use the line below if you're loading the features csv that has its first 0.05 and last 0.95 RT removed
    df = pd.read_csv(sys.argv[1], index_col=0)

    bin_time(df, rt_window=5, mz_window=1.0005079).to_csv("./rt5/"+name+"_window.csv")
