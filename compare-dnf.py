import argparse
import sys

#!/usr/bin/env python3

def parse_fedora_packages(file_path):
    """
    Parse the fedora-desktop-installed.txt file into a list of package information.
    
    Args:
        file_path (str): Path to the fedora-desktop-installed.txt file
    
    Returns:
        list: List of dictionaries containing package information, or None if error
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        packages = []
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and header
            if not line or line == "Pacotes instalados":
                continue
            
            # Split the line into components
            parts = line.split()
            if len(parts) >= 3:
                package_info = {
                    'full_name': parts[0],  # e.g., "Box2D.x86_64"
                    'name': parts[0].split('.')[0] if '.' in parts[0] else parts[0],  # e.g., "Box2D"
                    'architecture': parts[0].split('.')[1] if '.' in parts[0] else 'noarch',  # e.g., "x86_64"
                    'version': parts[1],  # e.g., "2.4.2-3.fc42"
                    'source': ' '.join(parts[2:])  # e.g., "781e4eb56ba449a5876af2cc084d758e"
                }
                packages.append(package_info)
        
        return packages
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return None
    except IOError as e:
        print(f"Error reading file: {e}")
        return None

def compare_package_lists(original, new):
    """
    Compare two lists of package information and identify added and removed packages.
    
    Args:
        original (list): List of package dictionaries from the original file
        new (list): List of package dictionaries from the new file
    
    Returns:
        tuple: (added_packages, removed_packages)
    """
    original_set = set(pkg['full_name'] for pkg in original)
    new_set = set(pkg['full_name'] for pkg in new)
    
    added_packages = new_set - original_set
    removed_packages = original_set - new_set
    
    return added_packages, removed_packages

def parse_fedora_packages_simple(file_path):
    """
    Parse the fedora-desktop-installed.txt file into a simple list of package names.
    
    Args:
        file_path (str): Path to the fedora-desktop-installed.txt file
    
    Returns:
        list: List of package names (without architecture), or None if error
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        packages = []
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and header
            if not line or line == "Pacotes instalados":
                continue
            
            # Extract just the package name (without architecture)
            parts = line.split()
            if len(parts) >= 1:
                full_name = parts[0]
                package_name = full_name.split('.')[0] if '.' in full_name else full_name
                packages.append(package_name)
        
        return packages
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return None
    except IOError as e:
        print(f"Error reading file: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Compare two text files')
    parser.add_argument('file1', help='First text file')
    parser.add_argument('file2', help='Second text file')
    
    args = parser.parse_args()
    
    try:
        with open(args.file1, 'r') as f1:
            content1 = f1.read()
        
        with open(args.file2, 'r') as f2:
            content2 = f2.read()
        
        print(f"File 1: {args.file1}")
        print(f"File 2: {args.file2}")
        print("Files loaded successfully")
        
        original_packages = parse_fedora_packages(args.file1)
        new_packages = parse_fedora_packages(args.file2)    
        
        added_packages, removed_packages = compare_package_lists(original_packages, new_packages)
        print("\nAdded Packages:")
        for pkg in removed_packages:
            print(" sudo dnf install " + pkg)
            
        print("Added Packages: " + format(len(removed_packages)))
        
        # print("\nRemoved Packages:")
        # for pkg in removed_packages:
        #     print(" > " + pkg)
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()