import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

#path = os.chdir('C:\\UF\\ABE4042C\\Autoanalyzer\\References')
path = os.chdir('C:/Users/jbarrett.carter/OneDrive/Research/PhD/Data/spectra/SN')
path = os.getcwd()
csv_files = glob.glob(os.path.join(path, "*.csv"))
data_df = pd.DataFrame()
max_values = []
min_values = []
avg_values = []
std_values = []
for f in csv_files:
    ref_df = pd.read_csv(f)
    max_values.append(ref_df['INT'].max())
    min_values.append(ref_df['INT'].min())
    avg_values.append(ref_df['INT'].mean())
    std_values.append(ref_df['INT'].std())
    data_df = pd.concat([data_df,ref_df])
    plt.plot(ref_df['WVL'], ref_df['INT'])
plt.show()
stats = pd.DataFrame(list(zip(min_values, max_values, avg_values, std_values)), columns = ['min','max','mean','std'])
stats = stats.T
stats['percent_diff'] = ((stats.max(axis=1)-stats.min(axis=1))/stats.max(axis=1))*100
data_df_stats = data_df['INT'].describe(include='all')
data_df_stats = data_df_stats.loc[['min','max','mean','std']]
stats['overall'] = data_df_stats

