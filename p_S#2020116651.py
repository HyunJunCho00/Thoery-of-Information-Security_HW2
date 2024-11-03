from oracle_python_v1_2 import pad_oracle
import sys

def confirm_padding(C0, C1):
    return pad_oracle(C0, C1) == b'1'

def hex_string_to_byte_array(s):
    return bytearray.fromhex(s)

def byte_array_to_hex_string(byte_array):
    return ''.join(f'{byte:02x}' for byte in byte_array)

def main(C0, C1):
    original_IV = hex_string_to_byte_array(C0[2:])  # Initialize original_IV with C0
    IV = bytearray([0x00] * 8)  # Initialize IV with 0x0000000000000000 (8 bytes)
    intermid = bytearray(8)
    for padding in range(1, 9):
        IV = bytearray([0x00] * 8)  # Reset IV to 0x0000000000000000 for each padding loop
        target_index = 8 - padding
        found = False
        for i in range(7, target_index, -1):
            IV[i] = intermid[i] ^ padding      
        for guess in range(256):
            IV[target_index] = guess
            modified_IV_hex = "0x" + byte_array_to_hex_string(IV)
            C1_hex = "0x" + C1[2:]
            if confirm_padding(modified_IV_hex, C1_hex):
                intermid[target_index] = guess ^ padding
                found = True
                break
        if not found:
            print(f"Failed to find correct padding for index {target_index}")
            print(f"Attempted IV: {byte_array_to_hex_string(IV)} for guess: {guess}")
            return 

    print("Original IV:", byte_array_to_hex_string(original_IV))
    plaintext = bytearray(original_IV[i] ^ intermid[i] for i in range(8))
    ascii_plaintext = ''.join(chr(b) for b in plaintext)
    print('----------------------------------------------')
    print("Recovered Plaintext (ASCII):", ascii_plaintext)
    print('----------------------------------------------')
# Usage example
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python ImprovedPaddingOracleAttack.py C0 C1")
    else:
        main(sys.argv[1], sys.argv[2])