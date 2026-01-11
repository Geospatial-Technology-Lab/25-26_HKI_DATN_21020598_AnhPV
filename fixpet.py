import os
import re
import glob
import shutil

def fix_pet_file(input_filepath, output_filepath):
    """Fix negative values in a single PET file and save to new location"""
    print(f"Processing {os.path.basename(input_filepath)}...")
    
    try:
        # Read the original file
        with open(input_filepath, 'r') as f:
            lines = f.readlines()
        
        if len(lines) < 6:
            print(f"  ⚠️ Warning: File has less than 6 lines (header expected)")
            return False
        
        # Keep header (first 6 lines), process data lines
        header = lines[:6]
        data_lines = lines[6:]
        
        # Count negative values found
        negative_count = 0
        processed_lines = []
        
        for line_num, line in enumerate(data_lines, start=7):
            original_line = line
            # Replace any negative number (including scientific notation) with 0
            # Pattern matches: -123, -123.456, -1.23e-4, -1.23E+5, etc.
            processed_line = re.sub(r'-\d+\.?\d*([eE][-+]?\d+)?', '0', line)
            
            # Count how many negative values were replaced in this line
            negative_count += len(re.findall(r'-\d+\.?\d*([eE][-+]?\d+)?', original_line))
            processed_lines.append(processed_line)
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
        
        # Write to new file
        with open(output_filepath, 'w') as f:
            f.writelines(header + processed_lines)
        
        print(f"  ✅ Fixed {negative_count} negative values → {os.path.basename(output_filepath)}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error processing file: {e}")
        return False

def verify_no_negatives(filepath):
    """Verify that no negative values remain in the file"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Skip header lines and check for negative numbers in data
        lines = content.split('\n')
        data_content = '\n'.join(lines[6:])  # Skip first 6 header lines
        
        negative_matches = re.findall(r'-\d+\.?\d*([eE][-+]?\d+)?', data_content)
        return len(negative_matches) == 0
    except:
        return False

def update_control_project(old_path, new_path):
    """Update the Control.Project file to use the new PETs folder"""
    control_file = "Control.Project"
    
    if not os.path.exists(control_file):
        print(f"⚠️ {control_file} not found. You'll need to manually update the PETPath.")
        return False
    
    try:
        # Read the control file
        with open(control_file, 'r') as f:
            content = f.read()
        
        # Update PETPath
        updated_content = re.sub(
            r'PETPath\s*=\s*"[^"]*"',
            f'PETPath\t\t=\t"./{new_path}/pet"',
            content
        )
        
        # Write back to file
        with open(control_file, 'w') as f:
            f.write(updated_content)
        
        print(f"✅ Updated {control_file}: PETPath changed to './{new_path}/pet'")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {control_file}: {e}")
        return False

def main():
    # Directory names
    original_pets_dir = "PETs"
    new_pets_dir = "PETs_fixed"
    
    # Check if original PETs directory exists
    if not os.path.exists(original_pets_dir):
        print(f"❌ Directory '{original_pets_dir}' not found!")
        print("Please make sure you're running this script from the correct directory.")
        return
    
    # Find all PET files in original directory
    pet_pattern = os.path.join(original_pets_dir, "pet*.asc")
    pet_files = glob.glob(pet_pattern)
    
    if not pet_files:
        print(f"❌ No PET files found in '{original_pets_dir}' directory")
        print(f"Looking for pattern: {pet_pattern}")
        return
    
    print(f"🔍 Found {len(pet_files)} PET files in '{original_pets_dir}'")
    print(f"📁 Creating new directory: '{new_pets_dir}'")
    print(f"📋 Original files will be preserved in '{original_pets_dir}'")
    print("=" * 60)
    
    # Create new directory
    os.makedirs(new_pets_dir, exist_ok=True)
    
    success_count = 0
    
    # Process each file
    for pet_file in sorted(pet_files):
        # Create corresponding output file path
        filename = os.path.basename(pet_file)
        output_file = os.path.join(new_pets_dir, filename)
        
        if fix_pet_file(pet_file, output_file):
            success_count += 1
        print()  # Empty line for readability
    
    print("=" * 60)
    print(f"📊 Processing Summary:")
    print(f"   Original directory: {original_pets_dir} (preserved)")
    print(f"   New directory: {new_pets_dir}")
    print(f"   Total files found: {len(pet_files)}")
    print(f"   Successfully processed: {success_count}")
    print(f"   Failed: {len(pet_files) - success_count}")
    
    if success_count > 0:
        # Verify results in new directory
        print(f"\n🔍 Verification of new files:")
        new_pet_files = glob.glob(os.path.join(new_pets_dir, "pet*.asc"))
        all_clean = True
        
        for pet_file in new_pet_files:
            if verify_no_negatives(pet_file):
                print(f"   ✅ {os.path.basename(pet_file)} - No negative values")
            else:
                print(f"   ❌ {os.path.basename(pet_file)} - Still has negative values!")
                all_clean = False
        
        if all_clean:
            print(f"\n🎉 SUCCESS! All PET files have been cleaned of negative values!")
            print(f"📁 Original files preserved in: {original_pets_dir}")
            print(f"📁 Fixed files created in: {new_pets_dir}")
            
            # Ask user if they want to update Control.Project
            print(f"\n🔧 Would you like to update Control.Project to use the new PET files?")
            response = input("Type 'yes' to update automatically, or 'no' to update manually: ").lower().strip()
            
            if response in ['yes', 'y']:
                if update_control_project(original_pets_dir, new_pets_dir):
                    print(f"\n🚀 Ready to run! Execute: ./iHydroSlide3D")
                else:
                    print(f"\n⚠️ Please manually update Control.Project:")
                    print(f"   Change: PETPath = \"./{original_pets_dir}/pet\"")
                    print(f"      To: PETPath = \"./{new_pets_dir}/pet\"")
            else:
                print(f"\n📝 Manual update required in Control.Project:")
                print(f"   Change: PETPath = \"./{original_pets_dir}/pet\"")
                print(f"      To: PETPath = \"./{new_pets_dir}/pet\"")
        else:
            print(f"\n⚠️ Some files still contain negative values. Please check manually.")
    
    # Show directory structure
    print(f"\n📂 Directory Structure:")
    print(f"   {original_pets_dir}/     ← Original PET files (preserved)")
    print(f"   {new_pets_dir}/     ← Fixed PET files (no negative values)")

if __name__ == "__main__":
    print("🚀 PET Files Negative Value Fixer (Preserve Original)")
    print("=" * 60)
    main()