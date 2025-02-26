import pandas as pd
from pathlib import Path

file = Path("D:/Repositories/25_01_Liver_Cancer/data/Microarray_Huh7_Modified.xlsx")
output_folder = Path("D:/Repositories/25_01_Liver_Cancer/data")
output_file = "Microarray_Huh7_normalized.txt"

df = pd.read_excel(file)
print(df.shape)
print(df.head())

df.to_csv(output_folder / output_file, sep='\t', index=False)

