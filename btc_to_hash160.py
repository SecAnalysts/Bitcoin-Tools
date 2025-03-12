import base58

def address_to_hash160(address):
    """
    Mengubah Bitcoin address (Base58Check) menjadi hash160 Compressed.
    """
    # Decode Base58Check address
    decoded = base58.b58decode_check(address)
    
    hash160 = decoded[1:].hex()
    return hash160

def main():
    input_file = "address_bitcoin.txt"
    
    # File output: Untuk menyimpan hash160 yang sudah di-compress
    output_file = "hash160_compressed.txt"
    
    with open(input_file, 'r') as file:
        addresses = file.read().splitlines()
    
    with open(output_file, 'w') as file:
        for address in addresses:
            try:
                hash160 = address_to_hash160(address)
                
                file.write(hash160 + '\n')
                print(f"Address: {address} -> Hash160: {hash160}")
            except Exception as e:
                print(f"Error processing address {address}: {e}")

if __name__ == "__main__":
    main()
