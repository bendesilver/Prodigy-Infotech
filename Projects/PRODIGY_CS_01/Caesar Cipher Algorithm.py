def caesar_cipher(text, shift):
    result = []
    for char in text:
        if char.isupper():
            base = ord('A')
        elif char.islower():
            base = ord('a')
        else:
            result.append(char)
            continue
        # Calculate the shifted character
        shifted = (ord(char) - base + shift) % 26
        result.append(chr(base + shifted))
    return ''.join(result)

print("Caesar Cipher Program")
mode = input("Do you want to encrypt or decrypt? ").strip().lower()
while mode not in ['encrypt', 'decrypt']:
    print("Invalid mode. Please enter 'encrypt' or 'decrypt'.")
    mode = input("Do you want to encrypt or decrypt? ").strip().lower()

message = input("Enter the message: ")
shift = int(input("Enter the shift value: "))

# Adjust shift for decryption
if mode == 'decrypt':
    shift = -shift

result = caesar_cipher(message, shift)

print(f"The {mode}ed message is: {result}")