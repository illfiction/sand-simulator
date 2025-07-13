from PIL import Image
from collections import Counter
img = Image.open("textures/sand.png").convert('RGB')

def load_palette_and_weights():
    pixels = list(img.getdata())

    color_counts = Counter(pixels)

    total = sum(color_counts.values())
    palette = list(color_counts.keys())


    probabilities = [count / total for count in color_counts.values()]

    return palette, probabilities
