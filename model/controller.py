from model.model import get_recommendations, features_list, model
from model.utils import extract_features
from config import UPLOAD_DIR
import os


def select_image_controller(img_id: str):
    # dir_path = '/home/rushikesh/Documents/projects/dl/Art-Recommendation/backend/resources/images/'
    selected_images_keys_list = [img_id]
    return get_recommendations(selected_images_keys_list)


def upload_image_controller(file_name_without_ext: str, file_name: str):
    dir_path = UPLOAD_DIR + '/'
    selected_images_keys_list = [file_name_without_ext]

    # extract features from the uploaded image
    features_list[file_name_without_ext] = extract_features(
        dir_path + file_name_without_ext + '.jpg', model)

    # get recommendations
    recommendations = get_recommendations(selected_images_keys_list)

    # clean up
    features_list.pop(file_name_without_ext)

    return recommendations


# print(select_image_controller('image_1000'))
