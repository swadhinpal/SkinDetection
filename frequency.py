import os
from PIL import Image

img1_folder = 'ibtd'
img2_folder = 'Mask'

# Initialize counters for screen and non-screen parts
total_screen_part_count = {}
total_non_screen_part_count = {}

# Get a list of filenames in each folder
files_folder1 = sorted(os.listdir(img1_folder))
files_folder2 = sorted(os.listdir(img2_folder))

# Iterate over the common indices
for i in range(min(len(files_folder1), len(files_folder2))):
    img1_filename = files_folder1[i]
    img2_filename = files_folder2[i]

    img1_path = os.path.join(img1_folder, img1_filename)
    img2_path = os.path.join(img2_folder, img2_filename)

    try:
        img1 = Image.open(img1_path)
        img2 = Image.open(img2_path)

        # Ensure both images have the same dimensions
        if img1.size != img2.size:
            raise ValueError(f"Images {img1_path} and {img2_path} must have the same dimensions.")

        width, height = img1.size

        # Loop through each pixel in the images
        for y in range(height):
            for x in range(width):
                pixel_img2 = img2.getpixel((x, y))

                # Check if pixel in img2 is white (>=225, >=225, >=225)
                if pixel_img2[0] >= 225 and pixel_img2[1] >= 225 and pixel_img2[2] >= 225:
                    pixel_img1 = img1.getpixel((x, y))

                    # Count occurrences for each pixel in img1
                    if pixel_img1 not in total_screen_part_count:
                        total_screen_part_count[pixel_img1] = 1
                    else:
                        total_screen_part_count[pixel_img1] += 1
                else:
                    # Count occurrences for non-screen parts
                    if pixel_img2 not in total_non_screen_part_count:
                        total_non_screen_part_count[pixel_img2] = 1
                    else:
                        total_non_screen_part_count[pixel_img2] += 1
    except Exception as e:
        print(f"Error processing {img1_path} and {img2_path}: {e}")

# Write frequencies to separate text files
screen_part_file_path = 'screen_part_frequencies.txt'
non_screen_part_file_path = 'non_screen_part_frequencies.txt'

with open(screen_part_file_path, 'w') as screen_file:
    for pixel, frequency in total_screen_part_count.items():
        screen_file.write(f"{pixel}: {frequency}\n")

with open(non_screen_part_file_path, 'w') as non_screen_file:
    for pixel, frequency in total_non_screen_part_count.items():
        non_screen_file.write(f"{pixel}: {frequency}\n")

# Print the accumulated frequencies
print("Total Frequency for Screen Part:")
print(total_screen_part_count)

print("\nTotal Frequency for Non-Screen Part:")
print(total_non_screen_part_count)
