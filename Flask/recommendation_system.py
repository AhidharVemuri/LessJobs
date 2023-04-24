# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 15:09:37 2023

@author: ahish
"""

import pandas as pd
import numpy as np
from sklearn.metrics import pairwise_distances

class RecommenderSystem:
    def __init__(self, num_recomm, metric = 'euclidean'):
        self.num_recomm = num_recomm
        self.metric = metric
    def fit(self, train_x, train_y):
        train_x = np.array(train_x)
        train_y = np.array(train_y)
        self.train_x = train_x
        self.train_y = train_y
    def predict(self,test_x):
        test_x = np.array(test_x).reshape((1,self.train_x.shape[1]))
        distances = pairwise_distances(test_x, self.train_x, metric = self.metric)
        distances = np.array(distances)
        indices = np.argsort(distances).flatten()
        indices = indices[:self.num_recomm]
        top_recommendations = self.train_y[indices]
        return top_recommendations
        
    
        
        












