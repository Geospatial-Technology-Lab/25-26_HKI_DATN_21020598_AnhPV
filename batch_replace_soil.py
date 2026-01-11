#!/usr/bin/env python3
"""
Script to batch replace values in Soil.asc file
Mapping: 7→3, 8→7, 9→6, 4 unchanged
"""

import os
import sys

def batch_replace_soil_values(input_file, output_file=None):
    """
    Replace values in Soil.asc file according to mapping:
    7 -> 3
    8 -> 7  
    9 -> 6
    4 -> 4 (unchanged)
    All other values remain unchanged
    """
    
    if output_file is None:
        output_file = input_file
    
    # Read the file
    print(f"Reading file: {input_file}")
    try:
        with open(input_file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File {input_file} not found!")
        return False
    except Exception as e:
        print(f"Error reading file: {e}")
        return False
    
    # Count original values
    original_counts = {
        '7': content.count(' 7 ') + content.count('\n7 ') + content.count(' 7\n'),
        '8': content.count(' 8 ') + content.count('\n8 ') + content.count(' 8\n'),
        '9': content.count(' 9 ') + content.count('\n9 ') + content.count(' 9\n'),
        '4': content.count(' 4 ') + content.count('\n4 ') + content.count(' 4\n')
    }
    
    print("Original value counts:")
    for val, count in original_counts.items():
        print(f"  Value {val}: {count} occurrences")
    
    # Perform replacements
    print("Performing batch replacements...")
    
    # Replace in order to avoid conflicts
    # First replace 9->6, then 8->7, then 7->3
    # This ensures no double-replacement occurs
    
    # Replace 9 with 6
    content = content.replace(' 9 ', ' 6 ')
    content = content.replace('\n9 ', '\n6 ')
    content = content.replace(' 9\n', ' 6\n')
    
    # Replace 8 with 7
    content = content.replace(' 8 ', ' 7 ')
    content = content.replace('\n8 ', '\n7 ')
    content = content.replace(' 8\n', ' 7\n')
    
    # Replace 7 with 3
    content = content.replace(' 7 ', ' 3 ')
    content = content.replace('\n7 ', '\n3 ')
    content = content.replace(' 7\n', ' 3\n')
    
    # Count new values
    new_counts = {
        '3': content.count(' 3 ') + content.count('\n3 ') + content.count(' 3\n'),
        '6': content.count(' 6 ') + content.count('\n6 ') + content.count(' 6\n'),
        '7': content.count(' 7 ') + content.count('\n7 ') + content.count(' 7\n'),
        '4': content.count(' 4 ') + content.count('\n4 ') + content.count(' 4\n')
    }
    
    print("New value counts:")
    for val, count in new_counts.items():
        print(f"  Value {val}: {count} occurrences")
    
    # Write the modified content
    try:
        with open(output_file, 'w') as f:
            f.write(content)
        print(f"Successfully wrote modified content to: {output_file}")
        return True
    except Exception as e:
        print(f"Error writing file: {e}")
        return False

def main():
    # Default file path
    soil_file = r"d:\Downloads\Compressed\iHydroSlide3D_v1_1\LandslideBasics\Soil.asc"
    
    # Check if file exists
    if not os.path.exists(soil_file):
        print(f"Error: File {soil_file} not found!")
        print("Please check the file path and try again.")
        sys.exit(1)
    
    # Create backup
    backup_file = soil_file + ".backup"
    print(f"Creating backup: {backup_file}")
    try:
        with open(soil_file, 'r') as src, open(backup_file, 'w') as dst:
            dst.write(src.read())
        print("Backup created successfully.")
    except Exception as e:
        print(f"Error creating backup: {e}")
        sys.exit(1)
    
    # Perform the replacement
    success = batch_replace_soil_values(soil_file)
    
    if success:
        print("\nBatch replacement completed successfully!")
        print("Mapping applied:")
        print("  7 → 3")
        print("  8 → 7") 
        print("  9 → 6")
        print("  4 → 4 (unchanged)")
        print(f"\nOriginal file backed up as: {backup_file}")
    else:
        print("\nBatch replacement failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
