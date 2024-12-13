
from backend import create_connection, fetch_random_characters
def encrypt_text_file(username, input_file, output_file):
    connection = create_connection()
    random_chars = fetch_random_characters(connection, username)
    if not random_chars:
        print(f"No random characters found for user {username}")
        return
    
    with open(input_file, 'r') as file:
        original_data = file.read()
    
    encrypted_data = ''.join(random_chars[ord(char) % len(random_chars)] for char in original_data)
    
    with open(output_file, 'w') as file:
        file.write(encrypted_data)
    
    print(f"File {input_file} has been encrypted and saved as {output_file}")
