
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

df = pd.read_csv('datasets/cosmetics.csv')
print(df.head())


plt.figure(figsize=(15, 20))
df.Brand.value_counts().head(20).plot(kind='barh')


#%%
sns.set_style('whitegrid')
treatment = df[df.Label=='Treatment']
price_treatment = treatment.groupby('Brand')[['Price']].mean().sort_values(by='Price', ascending=True)
price_treatment.plot(kind='barh', legend=False, figsize=(15,15))
plt.title('Avg price of treatment products by brand')


