import argparse
import sys
import tempfile
import os

#!/usr/bin/env python3

def parse_flatpak_packages(file_path):
    """
    Parse the fedora-flatpak-installed.txt file into a list of package information.

    Args:
        file_path (str): Path to the fedora-flatpak-installed.txt file

    Returns:
        list: List of dictionaries containing Flatpak package information, or None if error
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        packages = []

        for line in lines:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Split the line by tabs (Flatpak uses tab-separated format)
            parts = line.split('\t')
            if len(parts) >= 6:
                package_info = {
                    "name": parts[0],           # e.g., "Bambu Studio"
                    "app_id": parts[1],         # e.g., "com.bambulab.BambuStudio"
                    "version": parts[2],        # e.g., "2.3.0 Public Release"
                    "branch": parts[3],         # e.g., "stable"
                    "origin": parts[4],         # e.g., "flathub"
                    "installation": parts[5],   # e.g., "system" or "user"
                }
                packages.append(package_info)

        return packages

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return None
    except IOError as e:
        print(f"Error reading file: {e}")
        return None


def parse_fedora_packages(file_path):
    """
    Parse the fedora-desktop-installed.txt file into a list of package information.

    Args:
        file_path (str): Path to the fedora-desktop-installed.txt file

    Returns:
        list: List of dictionaries containing package information, or None if error
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
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
                    "full_name": parts[0],  # e.g., "Box2D.x86_64"
                    "name": parts[0].split(".")[0]
                    if "." in parts[0]
                    else parts[0],  # e.g., "Box2D"
                    "architecture": parts[0].split(".")[1]
                    if "." in parts[0]
                    else "noarch",  # e.g., "x86_64"
                    "version": parts[1],  # e.g., "2.4.2-3.fc42"
                    "source": " ".join(
                        parts[2:]
                    ),  # e.g., "781e4eb56ba449a5876af2cc084d758e"
                }
                packages.append(package_info)

        return packages

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return None
    except IOError as e:
        print(f"Error reading file: {e}")
        return None


def compare_package_lists(original, new, field="name"):
    """
    Compare two lists of package information and identify added and removed packages.

    Args:
        original (list): List of package dictionaries from the original file
        new (list): List of package dictionaries from the new file

    Returns:
        tuple: (added_packages, removed_packages)
    """
    original_set = set(pkg[field] for pkg in original)
    new_set = set(pkg[field] for pkg in new)

    added_packages = new_set - original_set
    removed_packages = original_set - new_set

    return added_packages, removed_packages


def main():
    parser = argparse.ArgumentParser(description="Compare two text files")
    parser.add_argument("file1", help="First text file")
    parser.add_argument("file2", help="Second text file")
    parser.add_argument("--is_flatpak", action="store_true", help="Parse files as Flatpak package lists instead of Fedora packages")
    args = parser.parse_args()

    try:
        with open(args.file1, "r") as f1:
            content1 = f1.read()

        with open(args.file2, "r") as f2:
            content2 = f2.read()

        print(f"File 1: {args.file1}")
        print(f"File 2: {args.file2}")
        print("Files loaded successfully")

        if args.is_flatpak:
            print("Comparing Flatpak package lists...")
            original_packages = parse_flatpak_packages(args.file1)
            new_packages = parse_flatpak_packages(args.file2)
            added_packages, removed_packages = compare_package_lists(
                original_packages, new_packages, "app_id"
        )
        else:
            print("Comparing Fedora package lists...")
            original_packages = parse_fedora_packages(args.file1)
            new_packages = parse_fedora_packages(args.file2)
            added_packages, removed_packages = compare_package_lists(
                original_packages, new_packages, "name"
            )


        print("Added Packages..: " + format(len(added_packages)))
        print("Removed Packages: " + format(len(removed_packages)))
        # Create temporary files for added and removed packages
        
        # Create temporary file for added packages
        if args.is_flatpak:
            command = "flatpak install "
        else:
            command = "dnf --skip-unavailable install "
        with tempfile.NamedTemporaryFile(mode='w', suffix='_added_packages.txt', delete=False) as added_file:
            added_file_path = added_file.name
            for pkg in added_packages:
                command += f"{pkg} "
            added_file.write(f"{command}\n")
        
        # Create temporary file for removed packages
        if args.is_flatpak:
            command = "flatpak install "
        else:
            command = "dnf --skip-unavailable install "
        with tempfile.NamedTemporaryFile(mode='w', suffix='_removed_packages.txt', delete=False) as removed_file:
            removed_file_path = removed_file.name
            for pkg in removed_packages:
                command += f"{pkg} "
            removed_file.write(f"{command}\n")
        
        print(f"Added packages written to: {added_file_path}")
        print(f"Removed packages written to: {removed_file_path}")


    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
