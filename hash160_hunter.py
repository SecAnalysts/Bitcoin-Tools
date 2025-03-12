import os
import hashlib
import coincurve

def load_hash160(filename):
    """Membaca file hash160.txt dan mengembalikan daftar hash160."""
    with open(filename, 'r') as file:
        return set(line.strip() for line in file)

def save_result(filename, private_key_hex, address, hash160):
    """Menyimpan hasil yang cocok ke file result.txt."""
    with open(filename, 'a') as file:
        file.write(f"Private Key (HEX): {private_key_hex}\n")
        file.write(f"Bitcoin Address: {address}\n")
        file.write(f"Hash160: {hash160}\n\n")

def generate_btc_address(hash160_set, result_file):
    """Mencari alamat Bitcoin yang cocok dengan daftar hash160."""
    counter = 0  # Counter untuk melacak jumlah percobaan
    while True:
        # Generate a random private key in HEX format
        private_key_hex = os.urandom(32).hex()
        
        # Calculate hash160
        private_key = bytes.fromhex(private_key_hex)
        public_key = coincurve.PublicKey.from_secret(private_key).format(compressed=True)  # Diubah ke compressed
        sha256_hash = hashlib.sha256(public_key).digest()
        ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
        pubkey_hash = ripemd160_hash.hex()
        
        # Increment counter
        counter += 1
        
        # Tampilkan status setiap 1.000.000 percobaan
        if counter % 1_000_000 == 0:
            print(f"Generated {counter:,} addresses...")
        
        # Check if the hash160 exists in the hash160 set
        if pubkey_hash in hash160_set:
            print(f"Match found after {counter:,} attempts!")
            print(f"Private Key (HEX): {private_key_hex}")
            print(f"Hash160: {pubkey_hash}")
            save_result(result_file, private_key_hex, "", pubkey_hash)

if __name__ == "__main__":
    # File yang berisi daftar hash160
    hash160_file = "hash160.txt"
    
    # File untuk menyimpan hasil yang cocok
    result_file = "result.txt"
    
    # Memuat daftar hash160 dari file
    hash160_set = load_hash160(hash160_file)
    
    # Menjalankan pencarian
    generate_btc_address(hash160_set, result_file)
