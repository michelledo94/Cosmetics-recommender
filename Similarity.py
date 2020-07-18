#!/usr/bin/env python
# coding: utf-8

# In[10]:


# Import libraries
import pandas as pd
import numpy as np
# from sklearn.manifold import TSNE
# from matplotlib import pyplot as plt
# from matplotlib.pyplot import figure
# import seaborn as sns
# import re, math
from collections import Counter


# In[4]:


# Load the data
df = pd.read_csv('datasets/cosmetics.csv')
df = df[~df.Ingredients.str.contains('Visit the DERMAFLASH boutique')]
# Check the first five rows
print(df.head())
print(df.Label.value_counts())


# In[209]:


class prod:
    def __init__(self, brand, label):
        self.brand = brand
        self.label = label

    def to_vector(self, inglist1, inglist2):
        cos1, cos2 = Counter(inglist1.split(', ')), Counter(inglist2.split(', '))
        words  = list(cos1.keys() | cos2.keys())
        vec1 = [cos1.get(word, 0) for word in words]
        vec2 = [cos2.get(word, 0) for word in words]
        return vec1, vec2

    def cosine(self, vec1, vec2):
        len_a  = sum(v1**2 for v1 in vec1) ** 0.5
        len_b  = sum(v2**2 for v2 in vec2) ** 0.5
        dot    = sum(v1*v2 for v1,v2 in zip(vec1, vec2))
        cosine = dot / (len_a * len_b)
        return cosine

    def recommend(self, new_list, df):
        scores = []
        for i in range(df.shape[1]):
            vec1, vec2 = self.to_vector(new_list, df.Ingredients[i])
            cs = self.cosine(vec1, vec2)
            scores.append(cs)
        return df.Name[np.argmax(scores)], df.Ingredients[np.argmax(scores)], scores[np.argmax(scores)]


# In[197]:


df.Label.value_counts()


# In[211]:


prod_moist = prod(label='Moisturizer', brand='Sephora')
print(prod_moist.label)


# In[208]:


new = 'Water\Aqua\Eau, Dimethicone, Butylene Glycol, Glycerin, Trisiloxane, Trehalose, Sucrose, Ammonium Acryloyldimethyltaurate/Vp Copolymer, Hydroxyethyl Urea, Camellia Sinensis (Green Tea) Leaf Extract, Silybum Marianum (LadyS Thistle) Extract, Betula Alba (Birch) Bark Extract, Saccharomyces Lysate Extract, Aloe Barbadensis Leaf Water, Thermus Thermophillus Ferment, Caffeine, Sorbitol, Palmitoyl Hexapeptide-12, Sodium Hyaluronate, Caprylyl Glycol, Oleth-10, Sodium Polyaspartate, Saccharide Isomerate, Hydrogenated Lecithin, Tocopheryl Acetate, Acrylates/C10-30 Alkyl Acrylate Crosspolymer, Glyceryl Polymethacrylate, Tromethamine, PEG-8, Hexylene Glycol, Magnesium Ascorbyl Phosphate, Disodium EDTA, BHT, Phenoxyethanol, Red 4 (CI 14700), Yellow 5 (CI 19140)'
prod_sephora = prod(brand='Sephora', label='Moisturizer')
print(prod_sephora.brand)
prod_sephora.recommend(new, df)


# In[167]:


import time
start_time = time.time()
cl = "Squalane, Aqua (Water), Coco-caprylate/caprate, Glycerin, Sucrose Stearate, Ethyl Macadamiate, Caprylic/capric Triglyceride, Sucrose Laurate, Hydrogenated Starch Hydrolysate, Sucrose Dilaurate, Sucrose Trilaurate, Polyacrylate Crosspolymer-6, Isoceteth-20, Sodium Polyacrylate, Tocopherol, Hydroxymethoxyphenyl Decanone, Trisodium Ethylenediamine Disuccinate, Malic Acid, Ethylhexylglycerin, Chlorphenesin."
prod_sephora.recommend(cl, df)
