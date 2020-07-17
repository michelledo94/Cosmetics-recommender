#%%
# Import libraries
import pandas as pd 
import numpy as np
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import seaborn as sns
import re, math
from collections import Counter
import os
os.chdir('C:\\Users\\bichn\\Desktop\\MSBA\\0 MOOCs\\abc')

#%%
# Load and clean data
df = pd.read_csv('datasets\cosmetics.csv')
df = df[~df.Ingredients.str.contains('Visit the DERMAFLASH boutique')]
#%%
class prod:
    """ 
    Process and output product recommendations with respect to retailer and product caregories
    """
    def __init__(self, retailer):
    
        self.retailer = retailer 
        
    def to_vector(self, inglist1, inglist2):
        """ 
        Take 2 ingredient lists and convert them to document-term frequency matrices/vectors used for next steps
        
        Arguments: 
            inglist1, inglist2: Ingredient lists 
            
        Return: 
            vec1, vec2: 2 vectors as inputs for calculating cosine score
        """
        cos1, cos2 = Counter(inglist1.split(', ')), Counter(inglist2.split(', '))
        words  = list(cos1.keys() | cos2.keys())
        vec1 = [cos1.get(word, 0) for word in words]    
        vec2 = [cos2.get(word, 0) for word in words]    
        return vec1, vec2

    def cosine(self, vec1, vec2): 
        """
        Calculate cosine similarity score
        """
        len_a  = sum(v1**2 for v1 in vec1) ** 0.5       
        len_b  = sum(v2**2 for v2 in vec2) ** 0.5             
        dot    = sum(v1*v2 for v1,v2 in zip(vec1, vec2))
        cosine = dot / (len_a * len_b) 
        return cosine 
    
    def recommend(self, new_list, df): 
        """ 
        Take ingredient list and return recommended product(s)
        Arguments:
            new_list: New ingredient list 
            df: data used to compare
        
        Return: 
            Name and ingredient list of recommended product(s)
        """
        scores = []
        for i in range(df.shape[1]):
            vec1, vec2 = self.to_vector(new_list, df.Ingredients[i])
            cs = self.cosine(vec1, vec2)
            scores.append(cs)
        return df.Name[np.argmax(scores)], df.Ingredients[np.argmax(scores)], scores[np.argmax(scores)]
    
#%%
new = 'Water\Aqua\Eau, Dimethicone, Butylene Glycol, Glycerin, Trisiloxane, Trehalose, Sucrose, Ammonium Acryloyldimethyltaurate/Vp Copolymer, Hydroxyethyl Urea, Camellia Sinensis (Green Tea) Leaf Extract, Silybum Marianum (LadyS Thistle) Extract, Betula Alba (Birch) Bark Extract, Saccharomyces Lysate Extract, Aloe Barbadensis Leaf Water, Thermus Thermophillus Ferment, Caffeine, Sorbitol, Palmitoyl Hexapeptide-12, Sodium Hyaluronate, Caprylyl Glycol, Oleth-10, Sodium Polyaspartate, Saccharide Isomerate, Hydrogenated Lecithin, Tocopheryl Acetate, Acrylates/C10-30 Alkyl Acrylate Crosspolymer, Glyceryl Polymethacrylate, Tromethamine, PEG-8, Hexylene Glycol, Magnesium Ascorbyl Phosphate, Disodium EDTA, BHT, Phenoxyethanol, Red 4 (CI 14700), Yellow 5 (CI 19140)'
prod_sephora = prod(retailer='Sephora')
print(prod_sephora.retailer)
prod_sephora.recommend(new, df)





