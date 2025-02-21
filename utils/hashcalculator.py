import hashlib

def calculate_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return f"File not found: {file_path}"

# Example usage for this custom package to calculate the SHA-256 hash of a file: {from lib.hashcalculator import calculate_file_hash}
# file_path = r"C:\Users\sumit\Desktop\Capstone\Backend\temp\vlc-3.0.21-win64.exe"
# file_hash = calculate_file_hash(file_path)
# print(f"SHA-256 hash of the file: {file_hash}")