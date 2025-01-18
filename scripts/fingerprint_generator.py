import os
import hashlib
import argparse

def hash_file(file_path):
    """Generate SHA-256 hash for a file."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def generate_fingerprint(directory, exclude=None, verbose=False):
    """Generate a fingerprint for a directory."""
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        return

    exclude = exclude or []
    file_hashes = []
    for root, _, files in os.walk(directory):
        for file in sorted(files):  # Sort files for consistency
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory)

            # Skip excluded files or directories
            if any(ex in relative_path for ex in exclude):
                if verbose:
                    print(f"Excluding: {relative_path}")
                continue

            file_hash = hash_file(file_path)
            file_hashes.append(f"{file_hash}  {relative_path}")

    # Create a combined fingerprint
    combined_hash = hashlib.sha256("\n".join(file_hashes).encode()).hexdigest()
    
    # Save to files
    with open("file_hashes.txt", "w") as fh:
        fh.write("\n".join(file_hashes))
    
    with open("project_fingerprint.txt", "w") as pf:
        pf.write(combined_hash)
    
    print("Fingerprinting complete.")
    print(f"Project Fingerprint: {combined_hash}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a fingerprint for a directory.")
    parser.add_argument("directory", help="Path to the directory to fingerprint.")
    parser.add_argument("--exclude", nargs="*", default=[], help="List of patterns to exclude.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")
    args = parser.parse_args()

    generate_fingerprint(args.directory, exclude=args.exclude, verbose=args.verbose)