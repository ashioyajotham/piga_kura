from cryptography.fernet import Fernet

def generate_fernet_key():
    """Generate a valid Fernet key and print it"""
    key = Fernet.generate_key()
    print(f"Generated Fernet key: {key.decode()}")
    print("\nAdd this to your .env file as:")
    print(f"VOTE_ENCRYPTION_KEY={key.decode()}")

if __name__ == "__main__":
    generate_fernet_key()
