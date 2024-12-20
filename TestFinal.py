from PIL import Image
import numpy as np
import os

# Read probabilities from text files
def read_probabilities(file_path):
    probabilities = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            pixel = tuple(map(int, parts[0][1:-1].split(',')))
            probability = float(parts[1].strip())
            probabilities[pixel] = probability
    return probabilities

# Calculate threshold
def calculate_threshold(sum_p_cs, sum_p_cns):
    return sum_p_cs / sum_p_cns

# Calculate sum of probabilities
def calculate_sum_of_probabilities(probabilities):
    return sum(probabilities.values())

# Check if a pixel should be drawn as (255, 255, 255) or (255, 0, 0) on img4
def decide_pixel_color(pixel, p_cs_probabilities, p_cns_probabilities, threshold):
    p_cs = p_cs_probabilities.get(pixel, 0)
    p_cns = p_cns_probabilities.get(pixel, 0)

    if p_cs == 0 and p_cns == 0:
        return (255, 255, 255)
    elif p_cs == 0:
        return (255, 255, 255)
    elif p_cns == 0:
        return (255, 255, 255)
    else:
        t1 = p_cs / p_cns
        if t1 >= threshold:
            return (255, 255, 255)
        else:
            return (255, 0, 0)

# Example usage
p_cs_file_path = 'p_cs_probabilities.txt'
p_cns_file_path = 'p_cns_probabilities.txt'

p_cs_probabilities = read_probabilities(p_cs_file_path)
p_cns_probabilities = read_probabilities(p_cns_file_path)

# Calculate sum of probabilities
sum_p_cs = calculate_sum_of_probabilities(p_cs_probabilities)
sum_p_cns = calculate_sum_of_probabilities(p_cns_probabilities)

# Calculate threshold
threshold = calculate_threshold(sum_p_cs, sum_p_cns)

# Load img3
img3_path = 'nure.jpg'  # Change this to the path of your img3
img3 = Image.open(img3_path)
width, height = img3.size

# Create img5
img5 = Image.new('RGB', (width, height))

# Get the filename without extension
filename, extension = os.path.splitext(os.path.basename(img3_path))

# Iterate through each pixel of img3 and decide color for img5
for y in range(height):
    for x in range(width):
        pixel = img3.getpixel((x, y))
        new_color = decide_pixel_color(pixel, p_cs_probabilities, p_cns_probabilities, threshold)
        img5.putpixel((x, y), new_color)

# Save img5 with 'z' added before the extension
img5_path = f'{filename}z' + extension
img5.save(img5_path)

# Print the path of img5
print(f'img5 saved at: {img5_path}')
