import os
import numpy as np
from keras.api.preprocessing import image
from keras.api.applications.resnet50 import preprocess_input
from tqdm import tqdm
import matplotlib.pyplot as plt
# import matplotlib.image as mpimg


def extract_features(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = model.predict(x).reshape(-1)
    return features


# def extract_features_from_directory(dir_path, model):
#     features_list = dict()
#     files = os.listdir(dir_path)
#     for file in tqdm(files):
#         features_list[file.replace('.jpg', '')] = extract_features(
#             (dir_path + file), model)
#     return features_list


def generate_datasets(selected_images_keys_list, features_list):
    dataset = []
    names = []
    selected_dataset = []
    selected_names = []
    for key, value in features_list.items():
        sw = 0
        for k in selected_images_keys_list:
            if key == k:
                selected_dataset.append(features_list[key])
                selected_names.append(key)
                sw = 1
        if sw == 0:
            dataset.append(value)
            names.append(key)
    return np.asarray(selected_names), np.asarray(selected_dataset), np.asarray(names), np.asarray(dataset)


def print_images(dir_path, selected_images_keys_list):
    fig = plt.figure()
    for i in range(len(selected_images_keys_list)):
        img_path = dir_path + selected_images_keys_list[i] + '.jpg'
        img = image.load_img(img_path, target_size=(224, 224))
        a = fig.add_subplot(
            1, len(selected_images_keys_list), i+1, autoscale_on=True)
        imgplot = plt.imshow(img)
        a.set_title(selected_images_keys_list[i])
        plt.axis('off')
