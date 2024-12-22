import numpy as np
from fpylll import LLL, IntegerMatrix

def read_public_key(file_path):
    """Read the public key matrix."""
    with open(file_path, 'r') as f:
        key = [list(map(int, line.split())) for line in f.readlines()]
    return np.array(key)

def read_cipher(file_path):
    """Read the ciphertext vector."""
    with open(file_path, 'r') as f:
        return np.array(list(map(int, f.read().split(','))))

def lattice_reduce(public_key):
    """Reduce the public key using the LLL algorithm."""
    mat = IntegerMatrix.from_matrix(public_key.tolist())
    reduced = LLL.reduction(mat)
    return np.array(reduced)

def closest_lattice_point(reduced_basis, ciphertext):
    """Find the closest lattice point to the ciphertext."""
    return np.round(np.linalg.solve(reduced_basis.T, ciphertext)).astype(int)

def decrypt(public_key, ciphertext):
    """Decrypt the ciphertext."""
    reduced_key = lattice_reduce(public_key)
    plaintext = []
    for c in ciphertext:
        # Map each ciphertext value to the closest lattice point
        point = closest_lattice_point(reduced_key, c)
        plaintext.append(chr(point[0]))  # Assuming 1D lattice for simplicity
    return ''.join(plaintext)

# Load data
public_key = read_public_key("public_key")
ciphertext = read_cipher("Cipher.txt")

# Decrypt
plaintext = decrypt(public_key, ciphertext)
if plaintext.startswith("I"):
    print("Decrypted Message:", plaintext)
else:
    print("Decryption Failed or Requires Adjustment")
