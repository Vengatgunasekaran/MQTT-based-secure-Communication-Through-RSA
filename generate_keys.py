from cryptography.fernet import Fernet

# Generate keys for each client
key1 = Fernet.generate_key()
key2 = Fernet.generate_key()
key3 = Fernet.generate_key()

# Display the keys
print("Client 1 Key:", key1.decode())
print("Client 2 Key:", key2.decode())
print("Client 3 Key:", key3.decode())
