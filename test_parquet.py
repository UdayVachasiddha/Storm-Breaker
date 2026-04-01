import pandas as pd
import traceback
import sys

with open('cols.txt', 'w') as f:
    try:
        df = pd.read_parquet('archive/UDP-training.parquet')
        f.write("UDP Rows:\n" + str(df[['Avg Packet Size', 'Flow IAT Mean', 'Packet Length Variance']].head(5)) + "\n")
        
        df_normal = pd.read_parquet('archive/UDP-testing.parquet') 
        # wait testing might still be attacks. 
        # Actually in CIC-DDoS2019, Label 'BENIGN' is normal traffic, others are attacks.
        f.write("\nLabels in UDP-training:\n" + str(df['Label'].value_counts()) + "\n")
    except Exception as e:
        f.write("Error: " + str(e) + "\n")
        f.write(traceback.format_exc())
