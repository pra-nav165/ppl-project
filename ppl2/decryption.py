from backend import create_connection, fetch_random_characters
def decrypt_text_file(username, input_file, output_file):
    connection = create_connection()
    random_chars = fetch_random_characters(connection, username)
    if not random_chars:
        print(f"No random characters found for user {username}")
        return
    
    # Create a reverse lookup dictionary for decryption
    reverse_lookup = {char: i for i, char in enumerate(random_chars)}
    
    with open(input_file, 'r') as file:
        encrypted_data = file.read()
    
    decrypted_data = ''.join(chr(reverse_lookup[char] % 256) for char in encrypted_data)
    
    with open(output_file, 'w') as file:
        file.write(decrypted_data)
    
    print(f"File {input_file} has been decrypted and saved as {output_file}")
