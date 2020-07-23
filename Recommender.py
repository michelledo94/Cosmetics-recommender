#%%
# Import libraries
import pandas as pd 
import numpy as np
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import seaborn as sns
import re
from collections import Counter
import os
import streamlit as st

# Set directory
os.chdir('C:\\Users\\bichn\\Desktop\\MSBA\\0 MOOCs\\Projects\\Cosmetics-recommender')

#%%
# Load and clean data
df = pd.read_csv('datasets/cosmetics.csv')
df = df[~df.Ingredients.str.contains('Visit the DERMAFLASH boutique')]

#%%
class prod:
    """ 
    Process and output product recommendations with respect to retailer and product caregories
    """
    def __init__(self, price, data, new_list):
        self.price = price
        self.data = data
        self.new_list = new_list
        
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
        len_1  = sum(v1**2 for v1 in vec1) ** 0.5       
        len_2  = sum(v2**2 for v2 in vec2) ** 0.5             
        dot    = sum(v1*v2 for v1,v2 in zip(vec1, vec2))
        cosine = dot / (len_1 * len_2) 
        return cosine 
    
    def get_scores(self): 
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
            vec1, vec2 = self.to_vector(self.new_list, df.Ingredients[i])
            cs = self.cosine(vec1, vec2)
            scores.append(cs)
        return scores
    
    def recommend(self):
        scores = self.get_scores()
        sim_idx = np.argmax(scores)
        if max(scores) >= 0.2 and df.Price[sim_idx] < self.price:
            sim_product = "{} {}".format(df.Brand[sim_idx], df.Name[sim_idx])
            return sim_product
        elif max(scores) >= 0.2 and df.Price[sim_idx] > self.price:
            return "No cheaper alternative found" 
        else:
            return "No similar product found"
    
    def get_prob(self):
        scores = self.get_scores()
        sim_idx = np.argmax(scores)
        if max(scores) >= 0.2 and df.Price[sim_idx] < self.price:
            prob = "{}%".format(round(scores[sim_idx]*100, 2))
        return prob 

    
#%%
if __name__ == "__main__":
    main()
