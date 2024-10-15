from generator.pixel_art_generator import PixelArtGenerator
import os
import random
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from config import NUM_IMAGES, IMAGE_WIDTH, IMAGE_HEIGHT, PIXEL_SIZE, TRAITS, TRAIT_OPTIONS, SEED, POST_PROCESSING, NUM_THREADS

def generate_and_save(i, generator, output_dir):
    image, metadata = generator.generate()
    image_path = os.path.join(output_dir, f"{i}.png")
    metadata_path = os.path.join(output_dir, f"{i}.json")
    generator.save_image(image, image_path)
    generator.save_metadata(metadata, metadata_path)
    print(f"Generated pixel art: {image_path}")

def main():
    if SEED is not None:
        random.seed(SEED)
        np.random.seed(SEED)

    generator = PixelArtGenerator(width=IMAGE_WIDTH, height=IMAGE_HEIGHT, pixel_size=PIXEL_SIZE, 
                                  traits=TRAITS, trait_options=TRAIT_OPTIONS, post_processing=POST_PROCESSING)
    
    output_dir = "data/output"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = [executor.submit(generate_and_save, i, generator, output_dir) for i in range(NUM_IMAGES)]
        for future in futures:
            future.result()

    print(f"Generated {NUM_IMAGES} pixel art images with metadata.")

if __name__ == "__main__":
    main()