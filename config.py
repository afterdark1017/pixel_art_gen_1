# Configuration settings for the Pixel Art Generator

# Number of images to generate
NUM_IMAGES = 100

# Image dimensions
IMAGE_WIDTH = 24
IMAGE_HEIGHT = 24
PIXEL_SIZE = 10

# Traits to include (set to False to omit)
TRAITS = {
    'background': True,
    'skin': True,
    'eyes': True,
    'mouth': True,
    'hair': True,
    'beard': True,
    'accessory': True
}

# Trait options with rarity weights (higher weight = more common)
TRAIT_OPTIONS = {
    'background': [('blue', 10), ('red', 10), ('green', 10), ('yellow', 10), ('purple', 5), ('orange', 5)],
    'skin': [('light', 10), ('medium', 10), ('dark', 10), ('alien', 2), ('zombie', 2)],
    'eyes': [('normal', 10), ('big', 5), ('small', 5), ('angry', 5), ('wink', 3), ('shades', 2)],
    'mouth': [('smile', 10), ('frown', 5), ('neutral', 10), ('open', 5), ('pipe', 2)],
    'hair': [('short', 10), ('long', 10), ('bald', 5), ('mohawk', 3), ('hat', 5), ('beanie', 3), ('cap', 5)],
    'beard': [('none', 15), ('stubble', 10), ('full', 5), ('goatee', 5)],
    'accessory': [('none', 20), ('earring', 10), ('necklace', 5), ('nose_ring', 5)]
}

# Seed for reproducible results (set to None for random generation)
SEED = None

# Post-processing options
POST_PROCESSING = {
    'noise': 0.1,  # Probability of adding noise to a pixel
    'blur': 0.5,   # Sigma for Gaussian blur (0 for no blur)
    'contrast': 1.2  # Contrast adjustment factor
}

# Number of threads for multi-threading
NUM_THREADS = 4