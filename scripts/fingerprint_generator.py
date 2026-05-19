import os
import hashlib
import argparse
import json
from fnmatch import fnmatch
from tqdm import tqdm
from datetime import datetime
from typing import List, Optional


def hash_file(file_path: str, algo: str = "sha256") -> str:
    """Generate a hash for a file using the specified algorithm."""
    hasher = hashlib.new(algo)
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def log(message: str):
    """Log a message with a timestamp."""
    print(f"[{datetime.now().isoformat()}] {message}")


def generate_fingerprint(
    directory: str,
    exclude: Optional[List[str]] = None,
    verbose: bool = False,
    algo: str = "sha256",
):
    """Generate a fingerprint for a directory."""
    if not os.path.isdir(directory):
        raise ValueError(f"{directory} is not a valid directory.")

    exclude = exclude or []
    file_hashes = []
    detailed_metadata = []

    for root, _, files in os.walk(directory):
        for file in tqdm(sorted(files), desc=f"Processing {root}"):
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory)

            # Skip excluded files or directories
            if any(fnmatch(relative_path, pattern) for pattern in exclude):
                if verbose:
                    log(f"Excluding: {relative_path}")
                continue

            try:
                file_hash = hash_file(file_path, algo=algo)
                file_size = os.path.getsize(file_path)
                modified_time = os.path.getmtime(file_path)

                # Append detailed metadata
                detailed_metadata.append({
                    "file_path": relative_path,
                    "hash": file_hash,
                    "size": file_size,
                    "modified_time": datetime.fromtimestamp(modified_time).isoformat()
                })

                file_hashes.append(f"{file_hash}  {relative_path}  {file_size}  {modified_time}")
            except Exception as e:
                log(f"Error processing {file_path}: {e}")
                continue

    # Create a combined fingerprint
    combined_hash = hashlib.new(algo, "\n".join(file_hashes).encode()).hexdigest()

    # Save to text files
    with open("file_hashes.txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(file_hashes))
    with open("project_fingerprint.txt", "w", encoding="utf-8") as pf:
        pf.write(combined_hash)

    # Save to JSON file
    with open("fingerprint.json", "w", encoding="utf-8") as jf:
        json.dump({"file_hashes": detailed_metadata, "combined_hash": combined_hash}, jf, indent=4)

    log("Fingerprinting complete.")
    log(f"Project Fingerprint: {combined_hash}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a fingerprint for a directory.")
    parser.add_argument("directory", help="Path to the directory to fingerprint.")
    parser.add_argument("--exclude", nargs="*", default=[], help="List of patterns to exclude.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")
    parser.add_argument("--hash-algo", default="sha256", choices=hashlib.algorithms_available, help="Hashing algorithm to use.")
    args = parser.parse_args()

    generate_fingerprint(args.directory, exclude=args.exclude, verbose=args.verbose, algo=args.hash_algo)