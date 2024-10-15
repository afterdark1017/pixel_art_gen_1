import os
from PIL import Image
import numpy as np

def load_image(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Image file not found: {file_path}")
    return np.array(Image.open(file_path))

def save_image(image, file_path):
    Image.fromarray(image.astype(np.uint8)).save(file_path)