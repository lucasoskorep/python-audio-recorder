import pandas as pd
import numpy as np

df = pd.read_csv("validated.tsv", sep="\t")

print(df.columns)

# print(df["accent"].unique())
# print(df["age"].unique())
# print(df["gender"].unique())
#
#

new_df = df[["path", "sentence", "age", "gender", "accent"]][0:0]

print(new_df)

new_df.to_csv("data.csv", sep=",", index=False)
