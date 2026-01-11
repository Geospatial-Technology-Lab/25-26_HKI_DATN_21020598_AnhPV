

# used to make the video

import cv2
import numpy as np
import glob
import os

# List of variable types to create videos for
variable_types = ['R', 'W', 'SM', 'FS', 'PF', 'Volume']

for var_type in variable_types:
    print(f"Creating video for {var_type}...")
    
    # Set path to the specific variable directory
    path = f'./{var_type}/'
    
    # Check if directory exists
    if not os.path.exists(path):
        print(f"Directory {path} does not exist, skipping {var_type}")
        continue
    
    # Get list of jpg files in the directory
    file_list = [f for f in os.listdir(path) if f.endswith('.jpg')]
    
    if not file_list:
        print(f"No jpg files found in {path}, skipping {var_type}")
        continue
    
    # Sort files by the numeric part in filename
    file_list = sorted(file_list, key=lambda x: int("".join([i for i in x if i.isdigit()])))
    
    print(f"Found {len(file_list)} images for {var_type}")
    
    # Read first image to get dimensions
    first_img = cv2.imread(path + file_list[0])
    if first_img is None:
        print(f"Could not read first image for {var_type}, skipping")
        continue
        
    height, width, layers = first_img.shape
    size = (width, height)
    
    # Create video writer
    output_filename = f'{var_type}.avi'
    out = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc(*'DIVX'), 5, size)
    
    # Add all images to video
    for filename in file_list:
        print(f"Processing {filename}")
        img = cv2.imread(path + filename)
        if img is not None:
            out.write(img)
    
    # Release video writer
    out.release()
    print(f"Video {output_filename} created successfully!")

print("All videos created!")

