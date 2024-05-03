import pickle
import os
import numpy as np
from keras.api.applications.resnet50 import ResNet50
from keras.api.preprocessing import image
from keras.api.applications.resnet50 import preprocess_input, decode_predictions
from scipy.spatial.distance import cdist
from model.utils import extract_features, generate_datasets, print_images
from typing import Dict


model = ResNet50(weights='imagenet', include_top=False)

with open('/home/rushikesh/Documents/projects/dl/Art-Recommendation/backend/resources/features_list.pkl', 'rb') as f:
    features_list: Dict = pickle.load(f)


def get_recommendations(selected_images_keys_list: list):
    topn = 5
    selected_names, selected_dataset, names, dataset = generate_datasets(
        selected_images_keys_list, features_list)
    distances = cdist(selected_dataset, dataset, 'cosine')

    recommendations = []
    for i in range(distances.shape[0]):
        nearest_ids = np.argsort(distances[i, :]).reshape(-1)[:topn]
        nearest_names = names[nearest_ids]
        recommendations.append(selected_names[i])
        for i in range(len(nearest_names)):
            recommendations.append(nearest_names[i])
        
    
    return recommendations
