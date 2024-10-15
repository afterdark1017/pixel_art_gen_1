import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import random
import json

class PixelArtGenerator:
    def __init__(self, width, height, pixel_size, traits, trait_options, post_processing):
        self.width = width
        self.height = height
        self.pixel_size = pixel_size
        self.traits = traits
        self.trait_options = trait_options
        self.post_processing = post_processing

    def generate(self):
        image = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        metadata = {}
        
        for trait, enabled in self.traits.items():
            if enabled:
                image, trait_value = getattr(self, f'_add_{trait}')(image)
                metadata[trait] = trait_value
        
        image = self._upscale_image(image)
        image = self._apply_post_processing(image)
        
        return image, metadata

    def _add_background(self, image):
        background = self._weighted_choice(self.trait_options['background'])
        color = self._get_color(background)
        return np.full((self.height, self.width, 3), color, dtype=np.uint8), background

    def _add_skin(self, image):
        skin_type = self._weighted_choice(self.trait_options['skin'])
        skin_color = self._get_color(skin_type)
        face_mask = self._create_face_mask()
        image[face_mask] = skin_color
        
        if skin_type == 'alien':
            image = self._add_alien_features(image)
        elif skin_type == 'zombie':
            image = self._add_zombie_features(image)
        
        return image, skin_type

    def _add_eyes(self, image):
        eye_type = self._weighted_choice(self.trait_options['eyes'])
        eye_color = [255, 255, 255]  # White
        pupil_color = [0, 0, 0]  # Black
        
        left_eye = (8, 10)
        right_eye = (15, 10)
        
        if eye_type == 'normal':
            self._draw_pixel(image, left_eye, eye_color)
            self._draw_pixel(image, right_eye, eye_color)
            self._draw_pixel(image, (left_eye[0], left_eye[1]+1), pupil_color)
            self._draw_pixel(image, (right_eye[0], right_eye[1]+1), pupil_color)
        elif eye_type == 'big':
            for i in range(-1, 2):
                for j in range(-1, 2):
                    self._draw_pixel(image, (left_eye[0]+i, left_eye[1]+j), eye_color)
                    self._draw_pixel(image, (right_eye[0]+i, right_eye[1]+j), eye_color)
            self._draw_pixel(image, left_eye, pupil_color)
            self._draw_pixel(image, right_eye, pupil_color)
        elif eye_type == 'small':
            self._draw_pixel(image, left_eye, pupil_color)
            self._draw_pixel(image, right_eye, pupil_color)
        elif eye_type == 'angry':
            self._draw_pixel(image, left_eye, eye_color)
            self._draw_pixel(image, right_eye, eye_color)
            self._draw_pixel(image, (left_eye[0], left_eye[1]-1), pupil_color)
            self._draw_pixel(image, (right_eye[0], right_eye[1]-1), pupil_color)
        elif eye_type == 'wink':
            self._draw_pixel(image, left_eye, eye_color)
            self._draw_pixel(image, (left_eye[0], left_eye[1]+1), pupil_color)
            self._draw_pixel(image, right_eye, pupil_color)
        elif eye_type == 'shades':
            shades_color = [50, 50, 50]
            for i in range(6, 18):
                self._draw_pixel(image, (i, 10), shades_color)
                self._draw_pixel(image, (i, 11), shades_color)
        
        return image, eye_type

    def _add_mouth(self, image):
        mouth_type = self._weighted_choice(self.trait_options['mouth'])
        mouth_color = [0, 0, 0]  # Black
        
        if mouth_type == 'smile':
            for i in range(9, 15):
                self._draw_pixel(image, (i, 18), mouth_color)
            self._draw_pixel(image, (8, 17), mouth_color)
            self._draw_pixel(image, (15, 17), mouth_color)
        elif mouth_type == 'frown':
            for i in range(9, 15):
                self._draw_pixel(image, (i, 16), mouth_color)
            self._draw_pixel(image, (8, 17), mouth_color)
            self._draw_pixel(image, (15, 17), mouth_color)
        elif mouth_type == 'neutral':
            for i in range(9, 15):
                self._draw_pixel(image, (i, 17), mouth_color)
        elif mouth_type == 'open':
            for i in range(9, 15):
                self._draw_pixel(image, (i, 17), mouth_color)
                self._draw_pixel(image, (i, 18), mouth_color)
            self._draw_pixel(image, (8, 17), mouth_color)
            self._draw_pixel(image, (15, 17), mouth_color)
        elif mouth_type == 'pipe':
            for i in range(9, 15):
                self._draw_pixel(image, (i, 17), mouth_color)
            self._draw_pixel(image, (15, 18), [139, 69, 19])  # Brown
            self._draw_pixel(image, (16, 18), [139, 69, 19])
            self._draw_pixel(image, (17, 17), [139, 69, 19])
        
        return image, mouth_type

    def _add_hair(self, image):
        hair_type = self._weighted_choice(self.trait_options['hair'])
        hair_color = self._get_random_hair_color()
        
        if hair_type == 'short':
            for i in range(6, 18):
                self._draw_pixel(image, (i, 5), hair_color)
            for i in range(5, 19):
                self._draw_pixel(image, (i, 6), hair_color)
        elif hair_type == 'long':
            for i in range(5, 19):
                for j in range(5, 8):
                    self._draw_pixel(image, (i, j), hair_color)
            for i in range(4, 20):
                self._draw_pixel(image, (i, 8), hair_color)
        elif hair_type == 'mohawk':
            for i in range(10, 14):
                for j in range(2, 8):
                    self._draw_pixel(image, (i, j), hair_color)
        elif hair_type == 'hat':
            hat_color = self._get_random_hat_color()
            for i in range(5, 19):
                for j in range(3, 7):
                    self._draw_pixel(image, (i, j), hat_color)
            for i in range(4, 20):
                self._draw_pixel(image, (i, 7), hat_color)
        elif hair_type == 'beanie':
            beanie_color = self._get_random_hat_color()
            for i in range(5, 19):
                for j in range(3, 7):
                    self._draw_pixel(image, (i, j), beanie_color)
            for i in range(6, 18):
                self._draw_pixel(image, (i, 2), beanie_color)
        elif hair_type == 'cap':
            cap_color = self._get_random_hat_color()
            for i in range(5, 19):
                for j in range(4, 7):
                    self._draw_pixel(image, (i, j), cap_color)
            for i in range(5, 15):
                self._draw_pixel(image, (i, 3), cap_color)
        
        return image, hair_type

    def _add_beard(self, image):
        beard_type = self._weighted_choice(self.trait_options['beard'])
        beard_color = self._get_random_hair_color()
        
        if beard_type == 'stubble':
            for i in range(8, 16):
                for j in range(19, 22):
                    if np.random.random() > 0.5:
                        self._draw_pixel(image, (i, j), beard_color)
        elif beard_type == 'full':
            for i in range(7, 17):
                for j in range(19, 23):
                    self._draw_pixel(image, (i, j), beard_color)
        elif beard_type == 'goatee':
            for i in range(10, 14):
                for j in range(19, 23):
                    self._draw_pixel(image, (i, j), beard_color)
        
        return image, beard_type

    def _add_accessory(self, image):
        accessory_type = self._weighted_choice(self.trait_options['accessory'])
        accessory_color = self._get_random_accessory_color()
        
        if accessory_type == 'earring':
            self._draw_pixel(image, (5, 13), accessory_color)
            self._draw_pixel(image, (5, 14), accessory_color)
        elif accessory_type == 'necklace':
            for i in range(9, 15):
                self._draw_pixel(image, (i, 22), accessory_color)
        elif accessory_type == 'nose_ring':
            self._draw_pixel(image, (12, 14), accessory_color)
        
        return image, accessory_type

    def _create_face_mask(self):
        mask = np.zeros((self.height, self.width), dtype=bool)
        center_y, center_x = self.height // 2, self.width // 2
        for y in range(self.height):
            for x in range(self.width):
                if ((x - center_x)**2 + (y - center_y)**2) <= (self.width//2)**2:
                    mask[y, x] = True
        return mask

    def _get_color(self, color_name):
        colors = {
            'blue': [0, 0, 255],
            'red': [255, 0, 0],
            'green': [0, 255, 0],
            'yellow': [255, 255, 0],
            'purple': [128, 0, 128],
            'orange': [255, 165, 0],
            'light': [255, 224, 189],
            'medium': [241, 194, 125],
            'dark': [141, 85, 36],
            'alien': [0, 255, 0],
            'zombie': [144, 238, 144]
        }
        return colors.get(color_name, [0, 0, 0])

    def _get_random_hair_color(self):
        colors = [
            [0, 0, 0],       # Black
            [165, 42, 42],   # Brown
            [255, 215, 0],   # Blonde
            [255, 0, 0],     # Red
            [128, 128, 128]  # Gray
        ]
        return colors[np.random.randint(0, len(colors))]

    def _get_random_hat_color(self):
        colors = [
            [255, 0, 0],     # Red
            [0, 0, 255],     # Blue
            [0, 255, 0],     # Green
            [255, 255, 0],   # Yellow
            [128, 0, 128],   # Purple
            [255, 165, 0]    # Orange
        ]
        return colors[np.random.randint(0, len(colors))]

    def _get_random_accessory_color(self):
        colors = [
            [255, 215, 0],   # Gold
            [192, 192, 192], # Silver
            [255, 0, 0],     # Red
            [0, 0, 255],     # Blue
            [0, 255, 0]      # Green
        ]
        return colors[np.random.randint(0, len(colors))]

    def _draw_pixel(self, image, position, color):
        x, y = position
        if 0 <= x < self.width and 0 <= y < self.height:
            image[y, x] = color

    def _add_alien_features(self, image):
        # Add antenna
        antenna_color = [0, 200, 0]
        self._draw_pixel(image, (11, 1), antenna_color)
        self._draw_pixel(image, (12, 1), antenna_color)
        self._draw_pixel(image, (11, 2), antenna_color)
        self._draw_pixel(image, (12, 2), antenna_color)
        return image

    def _add_zombie_features(self, image):
        # Add some green tint and "wounds"
        wound_color = [139, 0, 0]  # Dark red
        for y in range(self.height):
            for x in range(self.width):
                if image[y, x].tolist() == self._get_color('zombie'):
                    if np.random.random() < 0.1:
                        image[y, x] = wound_color
        return image

    def _upscale_image(self, image):
        return np.repeat(np.repeat(image, self.pixel_size, axis=0), self.pixel_size, axis=1)

    def _weighted_choice(self, options):
        total = sum(weight for _, weight in options)
        r = random.uniform(0, total)
        upto = 0
        for choice, weight in options:
            if upto + weight >= r:
                return choice
            upto += weight
        assert False, "Shouldn't get here"

    def _apply_post_processing(self, image):
        # Convert to PIL Image for post-processing
        pil_image = Image.fromarray(image.astype(np.uint8))
        
        # Add noise
        if self.post_processing['noise'] > 0:
            noise = np.random.randint(0, 255, image.shape, dtype=np.uint8)
            noise_mask = np.random.random(image.shape[:2]) < self.post_processing['noise']
            pil_image = Image.fromarray(np.where(noise_mask[:,:,None], noise, image).astype(np.uint8))
        
        # Apply blur
        if self.post_processing['blur'] > 0:
            pil_image = pil_image.filter(ImageFilter.GaussianBlur(self.post_processing['blur']))
        
        # Adjust contrast
        if self.post_processing['contrast'] != 1:
            enhancer = ImageEnhance.Contrast(pil_image)
            pil_image = enhancer.enhance(self.post_processing['contrast'])
        
        return np.array(pil_image)

    def save_image(self, image, file_path):
        Image.fromarray(image.astype(np.uint8)).save(file_path)

    def save_metadata(self, metadata, file_path):
        with open(file_path, 'w') as f:
            json.dump(metadata, f, indent=2)