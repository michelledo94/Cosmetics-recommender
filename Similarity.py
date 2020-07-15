#!/usr/bin/env python
# coding: utf-8

# In[10]:


# Import libraries
import pandas as pd
import numpy as np
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import seaborn as sns
import re, math
from collections import Counter


# In[4]:


# Load the data
df = pd.read_csv('datasets/cosmetics.csv')
df = df[~df.Ingredients.str.contains('Visit the DERMAFLASH boutique')]
# Check the first five rows 
display(df.head())


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
prod_sephora = prod(brand='Sephora')
print(prod_sephora.brand)
prod_sephora.recommend(new, df)


# In[167]:


import time
start_time = time.time()
cl = "Squalane, Aqua (Water), Coco-caprylate/caprate, Glycerin, Sucrose Stearate, Ethyl Macadamiate, Caprylic/capric Triglyceride, Sucrose Laurate, Hydrogenated Starch Hydrolysate, Sucrose Dilaurate, Sucrose Trilaurate, Polyacrylate Crosspolymer-6, Isoceteth-20, Sodium Polyacrylate, Tocopherol, Hydroxymethoxyphenyl Decanone, Trisodium Ethylenediamine Disuccinate, Malic Acid, Ethylhexylglycerin, Chlorphenesin."
prod.recommend(cl, df)


# In[203]:


sun = "Avobenzone, Homosalate, Octisalate. Inactive: Aqua/Water/Eau, Butyloctyl Salicylate, Pentylene Glycol, Lactococcus Ferment Lysate, 1,2-Hexanediol, Silica, Ectoin, Glycerin, Arginine, Hydroxyectoin, Ananas Sativus (Pineapple) Fruit Extract, Carica Papaya (Papaya) Fruit Extract, Lactic Acid, Camellia Sinensis Leaf Extract, Hedychium Coronarium Root Extract, Triethyl Citrate, Citrus Aurantium Dulcis (Orange) Peel Extract, Citrus Limon (Lemon) Peel Extract, Pyrus Communis (Pear) Fruit Extract), Pyrus Malus (Apple) Fruit Extract, Rubus Idaeus (Raspberry) Fruit Extract, Vanilla Planifolia Fruit Extract, Pimpinella Anisum Fruit Extract, Mica, Tocopherol, Ammonium Acryloyldimethyltaurate/VP Copolymer, Synthetic Fluorphlogopite, Hydrolyzed Wheat Protein/PVP Crosspolymer, Carbomer, Dibutyl Lauroyl Glutamide, Dibutyl Ethylhexanoyl Glutamide, Propanediol, Trisodium Ethylenediamine Disuccinate, Sodium Chloride, Sodium Benzoate, Ehtylhexylglycerin, Tin Oxide, Phenoxyethanol."
prod.recommend(sun, df)


# In[199]:


df[df.Name=='The Water Cream']


# In[196]:


c = sorted(cl.split(', '))
ing = df[df.Name=='Ultra Facial Cream']
n = sorted(list(ing.Ingredients)[0].split(', '))
count = 0
for i in c:
    if i in n:
        count+=1
print(count)
print(c)
print(n)


# Squalane, Aqua (Water), Coco-caprylate/caprate, Glycerin, Sucrose Stearate, Ethyl Macadamiate, Caprylic/capric Triglyceride, Sucrose Laurate, Hydrogenated Starch Hydrolysate, Sucrose Dilaurate, Sucrose Trilaurate, Polyacrylate Crosspolymer-6, Isoceteth-20, Sodium Polyacrylate, Tocopherol, Hydroxymethoxyphenyl Decanone, Trisodium Ethylenediamine Disuccinate, Malic Acid, Ethylhexylglycerin, Chlorphenesin.

# In[130]:


text1 = df.Ingredients[0]
text2 = df.Ingredients[1]

v1, v2 = prod.to_vector(text1, text2)
prod.cosine(v1, v2)


# In[82]:


WORD = re.compile(r"\w+")


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


# In[124]:


vec1 = text_to_vector(''.join(df.Ingredients[3].split(',')))
vec2 = text_to_vector(''.join(df.Ingredients[6].split(',')))
get_cosine(vec1, vec2)

