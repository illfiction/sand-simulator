from PIL import Image
from collections import Counter
img = Image.open("textures/sand.png").convert('RGB')

def load_palette_and_weights(material):
    image_str = f"textures/{material}.png"

    img = Image.open(image_str).convert('RGB')
    pixels = list(img.getdata())

    color_counts = Counter(pixels)

    total = sum(color_counts.values())
    palette = list(color_counts.keys())


    probabilities = [count / total for count in color_counts.values()]

    return palette, probabilities
