from PIL import Image
import numpy as np

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
        return (255, 0, 0)
    else:
        t1 = p_cs / p_cns
        if t1 >= threshold:
            return (255, 0, 0)
        else:
            return (255, 255, 255)

# Example usage
p_cs_file_path = 'p_cs_probabilities.txt'
p_cns_file_path = 'p_cns_probabilities.txt'

p_cs_probabilities = read_probabilities(p_cs_file_path)
p_cns_probabilities = read_probabilities(p_cns_file_path)

# Calculate threshold
sum_p_cs = calculate_sum_of_probabilities(p_cs_probabilities)
sum_p_cns = calculate_sum_of_probabilities(p_cns_probabilities)
threshold = calculate_threshold(sum_p_cs, sum_p_cns)

# Load img3
img3_path = 'test3.jpg'  # Change this to the path of your img3
img3 = Image.open(img3_path)
width, height = img3.size

# Create img4
img4 = Image.new('RGB', (width, height))

# Iterate through each pixel of img3 and decide color for img4
for y in range(height):
    for x in range(width):
        pixel = img3.getpixel((x, y))
        new_color = decide_pixel_color(pixel, p_cs_probabilities, p_cns_probabilities, threshold)
        img4.putpixel((x, y), new_color)

# Save img4
img4.save('img4.jpg')  # Change this to the desired path for img4
