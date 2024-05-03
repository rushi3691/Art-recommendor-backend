
import os
import numpy as np
from config import IMAGES_DIR

def get_all_images_list():
    global IMAGES_DIR
    return os.listdir(IMAGES_DIR)


def get_some_random_images():
    global IMAGES_DIR
    images = get_all_images_list()
    np.random.shuffle(images)
    return images[:5]
